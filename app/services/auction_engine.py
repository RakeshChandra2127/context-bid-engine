from dataclasses import dataclass
from typing import List, Optional
from app.models import Campaign

@dataclass
class AuctionCandidate:
    campaign_id: int
    campaign: Campaign
    bid_amount_cents: int
    relevance_score: float
    effective_bid: float = 0.0
    
    def __post_init__(self):
        self.effective_bid = float(self.bid_amount_cents) * self.relevance_score

@dataclass
class AuctionResult:
    winner: Optional[AuctionCandidate]
    clearing_price_cents: int
    all_candidates: List[AuctionCandidate]
    auction_type: str = 'second_price'

class AuctionEngine:
    """
    Implements a Real-Time Bidding (RTB) auction engine.
    
    This engine uses a Second-Price Auction (Vickrey auction) model.
    In a second-price auction, the highest bidder wins the ad slot, but pays the price
    offered by the second-highest bidder plus a nominal increment (e.g., 1 cent).
    
    Why second-price?
    It is computationally simple and strategically "incentive compatible."
    It encourages bidders to bid their true maximum value for the impression, 
    because bidding higher won't necessarily make them pay more (unless it changes who wins),
    and bidding lower risks losing the auction while not reducing the price they would have paid if they won.
    """
    
    def __init__(self, min_relevance_score: float = 0.1, auction_type: str = 'second_price'):
        self.min_relevance_score = min_relevance_score
        self.auction_type = auction_type

    def run_auction(self, candidates: List[AuctionCandidate], max_winners: int = 1) -> AuctionResult:
        """
        Runs the auction given a list of candidates.
        """
        # 1. Filter by relevance
        valid_candidates = [c for c in candidates if c.relevance_score >= self.min_relevance_score]
        
        # 2. Filter by budget exhaustion
        valid_candidates = [
            c for c in valid_candidates 
            if (c.campaign.spent_today_cents or 0) < c.campaign.daily_budget_cents
        ]
        
        # 3. Sort by effective bid descending
        sorted_candidates = sorted(valid_candidates, key=lambda c: c.effective_bid, reverse=True)
        
        if not sorted_candidates:
            return AuctionResult(winner=None, clearing_price_cents=0, all_candidates=candidates, auction_type=self.auction_type)
            
        winner = sorted_candidates[0]
        
        # Determine clearing price (second-price auction)
        if self.auction_type == 'second_price':
            if len(sorted_candidates) > 1:
                # The clearing price is the effective bid of the second highest bidder divided by the winner's relevance
                # This ensures the clearing price respects the second highest effective bid
                second_highest_effective_bid = sorted_candidates[1].effective_bid
                # Convert back to cents, adding 1 cent
                clearing_price = int(second_highest_effective_bid / winner.relevance_score) + 1
            else:
                # Floor price if only one candidate (e.g., 1 cent or a configured floor)
                clearing_price = 1
        else:
            # First price auction
            clearing_price = winner.bid_amount_cents
            
        # Ensure clearing price doesn't exceed the winner's original bid
        clearing_price = min(clearing_price, winner.bid_amount_cents)
            
        return AuctionResult(
            winner=winner,
            clearing_price_cents=clearing_price,
            all_candidates=sorted_candidates,
            auction_type=self.auction_type
        )
