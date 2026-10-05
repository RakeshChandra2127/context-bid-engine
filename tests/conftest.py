import pytest
import pytest_asyncio
from app.schemas import ContentAnalysis
from app.models import Campaign
from app.services.auction_engine import AuctionCandidate

@pytest.fixture
def sample_content_analysis():
    return ContentAnalysis(
        categories=["IAB1", "IAB2"],
        sentiment="positive",
        keywords=["test", "ad"]
    )

@pytest.fixture
def sample_campaigns():
    return [
        Campaign(id=1, advertiser_id=1, name="C1", max_bid_cents=100, budget_daily_cents=1000, spent_today_cents=0, is_active=True, ad_title="T1", ad_body="B1", ad_url="U1"),
        Campaign(id=2, advertiser_id=2, name="C2", max_bid_cents=50, budget_daily_cents=1000, spent_today_cents=0, is_active=True, ad_title="T2", ad_body="B2", ad_url="U2")
    ]

@pytest.fixture
def sample_auction_candidates(sample_campaigns):
    return [
        AuctionCandidate(campaign=sample_campaigns[0], relevance_score=0.9),
        AuctionCandidate(campaign=sample_campaigns[1], relevance_score=0.8)
    ]
