from app.services.auction_engine import AuctionEngine, AuctionCandidate
from app.models import Campaign

def test_second_price_auction_winner_pays_second_highest():
    engine = AuctionEngine()
    c1 = Campaign(id=1, max_bid_cents=100, budget_daily_cents=1000, spent_today_cents=0)
    c2 = Campaign(id=2, max_bid_cents=50, budget_daily_cents=1000, spent_today_cents=0)
    
    candidates = [
        AuctionCandidate(campaign=c1, relevance_score=1.0),
        AuctionCandidate(campaign=c2, relevance_score=1.0)
    ]
    
    results = engine.run_auction(candidates, floor_price=10, max_ads=1)
    assert len(results) == 1
    assert results[0].campaign.id == 1
    assert results[0].winning_price_cents == 51  # 50 + 1 (second highest bid + 1 cent)

def test_single_candidate_pays_floor_price():
    engine = AuctionEngine()
    c1 = Campaign(id=1, max_bid_cents=100, budget_daily_cents=1000, spent_today_cents=0)
    candidates = [AuctionCandidate(campaign=c1, relevance_score=1.0)]
    
    results = engine.run_auction(candidates, floor_price=10, max_ads=1)
    assert len(results) == 1
    assert results[0].winning_price_cents == 10

def test_no_candidates_returns_none():
    engine = AuctionEngine()
    results = engine.run_auction([], floor_price=10, max_ads=1)
    assert len(results) == 0

def test_low_relevance_filtered_out():
    engine = AuctionEngine()
    c1 = Campaign(id=1, max_bid_cents=100, budget_daily_cents=1000, spent_today_cents=0)
    candidates = [AuctionCandidate(campaign=c1, relevance_score=0.1)] # Below default threshold of 0.3
    
    results = engine.run_auction(candidates, floor_price=10, max_ads=1)
    assert len(results) == 0

def test_exhausted_budget_filtered_out():
    engine = AuctionEngine()
    c1 = Campaign(id=1, max_bid_cents=100, budget_daily_cents=1000, spent_today_cents=1000)
    candidates = [AuctionCandidate(campaign=c1, relevance_score=1.0)]
    
    results = engine.run_auction(candidates, floor_price=10, max_ads=1)
    assert len(results) == 0

def test_effective_bid_calculation():
    # max_bid * relevance_score
    engine = AuctionEngine()
    c1 = Campaign(id=1, max_bid_cents=100, budget_daily_cents=1000, spent_today_cents=0)
    cand = AuctionCandidate(campaign=c1, relevance_score=0.5)
    assert cand.effective_bid == 50.0

def test_multiple_winners():
    engine = AuctionEngine()
    c1 = Campaign(id=1, max_bid_cents=100, budget_daily_cents=1000, spent_today_cents=0)
    c2 = Campaign(id=2, max_bid_cents=80, budget_daily_cents=1000, spent_today_cents=0)
    c3 = Campaign(id=3, max_bid_cents=50, budget_daily_cents=1000, spent_today_cents=0)
    
    candidates = [
        AuctionCandidate(campaign=c1, relevance_score=1.0),
        AuctionCandidate(campaign=c2, relevance_score=1.0),
        AuctionCandidate(campaign=c3, relevance_score=1.0)
    ]
    
    results = engine.run_auction(candidates, floor_price=10, max_ads=2)
    assert len(results) == 2
    assert results[0].campaign.id == 1
    assert results[0].winning_price_cents == 81
    assert results[1].campaign.id == 2
    assert results[1].winning_price_cents == 51
