import time
import uuid
import logging
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models import Campaign, AuctionLog
from app.schemas import AdResponse, ServedAd, ContentAnalysis
from app.config import get_settings
from app.services.content_fetcher import ContentFetcher
from app.services.cache_service import CacheService
from app.services.content_analyzer import ContentAnalyzer
from app.services.auction_engine import AuctionEngine, AuctionCandidate

logger = logging.getLogger(__name__)

class AdSelector:
    def __init__(self, cache_service: CacheService):
        self.settings = get_settings()
        self.cache_service = cache_service
        self.fetcher = ContentFetcher()
        self.analyzer = ContentAnalyzer()
        self.auction_engine = AuctionEngine(
            min_relevance_score=self.settings.MIN_RELEVANCE_SCORE,
            auction_type='second_price' if self.settings.AUCTION_SECOND_PRICE else 'first_price'
        )

    def _calculate_relevance(self, campaign: Campaign, analysis: ContentAnalysis) -> float:
        if not campaign.target_categories or not analysis.categories:
            return 0.0
            
        max_confidence = 0.0
        campaign_targets = set(campaign.target_categories)
        
        for category in analysis.categories:
            if category.code in campaign_targets:
                if category.confidence > max_confidence:
                    max_confidence = category.confidence
                    
        return max_confidence

    def _build_response(
        self, 
        request_id: str, 
        winner: Optional[AuctionCandidate], 
        clearing_price: int, 
        analysis: ContentAnalysis, 
        processing_time_ms: int
    ) -> AdResponse:
        served_ads = []
        if winner:
            ad = ServedAd(
                campaign_id=winner.campaign_id,
                ad_markup=winner.campaign.ad_markup,
                clearing_price_cents=clearing_price,
                relevance_score=winner.relevance_score
            )
            served_ads.append(ad)
            
        return AdResponse(
            request_id=request_id,
            served_ads=served_ads,
            content_analysis=analysis,
            processing_time_ms=processing_time_ms
        )

    async def select_ads(
        self, 
        content: str, 
        url: Optional[str], 
        max_ads: int, 
        db: AsyncSession
    ) -> AdResponse:
        request_id = str(uuid.uuid4())
        start_time = time.time()
        
        # 1. Get content (if URL provided and content empty)
        text_to_analyze = content
        if url and not content:
            text_to_analyze = await self.fetcher.fetch_page_content(url)
            
        if not text_to_analyze:
            text_to_analyze = "Empty content"
            
        # 2. Hash and Cache check
        content_hash = self.fetcher.compute_content_hash(text_to_analyze)
        analysis = await self.cache_service.get_analysis(content_hash)
        
        # 3. Analyze if cache miss
        if not analysis:
            analysis = await self.analyzer.analyze_content(text_to_analyze)
            await self.cache_service.set_analysis(
                content_hash, 
                analysis, 
                self.settings.CACHE_TTL_SECONDS
            )
            
        # 4. Query active campaigns
        # Simplified query for now; ideally we filter by targeting here if database supports array overlap
        result = await db.execute(select(Campaign).where(Campaign.is_active == True))
        active_campaigns = result.scalars().all()
        
        # 5. Build candidates
        candidates = []
        for campaign in active_campaigns:
            relevance = self._calculate_relevance(campaign, analysis)
            if relevance > 0:
                candidate = AuctionCandidate(
                    campaign_id=campaign.id,
                    campaign=campaign,
                    bid_amount_cents=campaign.max_bid_cents,
                    relevance_score=relevance
                )
                candidates.append(candidate)
                
        # 6. Run Auction
        auction_result = self.auction_engine.run_auction(candidates, max_winners=max_ads)
        
        # 7. Log auction
        if auction_result.winner:
            log_entry = AuctionLog(
                request_id=request_id,
                campaign_id=auction_result.winner.campaign_id,
                winning_bid_cents=auction_result.winner.bid_amount_cents,
                clearing_price_cents=auction_result.clearing_price_cents,
                relevance_score=auction_result.winner.relevance_score
            )
            db.add(log_entry)
            try:
                await db.commit()
            except Exception as e:
                logger.error(f"Failed to log auction: {e}")
                await db.rollback()
                
        processing_time_ms = int((time.time() - start_time) * 1000)
        
        return self._build_response(
            request_id,
            auction_result.winner,
            auction_result.clearing_price_cents,
            analysis,
            processing_time_ms
        )
