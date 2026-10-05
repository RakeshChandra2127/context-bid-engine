from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.types import JSON as SAJSON

from app.database import Base


class AuctionLog(Base):
    """Auction Log model."""

    __tablename__ = "auction_log"

    id = Column(Integer, primary_key=True)
    request_id = Column(String(36), nullable=False)
    page_url = Column(String(2000), nullable=True)
    page_context_hash = Column(String(64))
    detected_categories = Column(SAJSON)
    detected_topics = Column(SAJSON)
    winning_campaign_id = Column(Integer, ForeignKey("campaign.id"), nullable=True)
    winning_bid_cents = Column(Integer, nullable=True)
    clearing_price_cents = Column(Integer, nullable=True)
    candidates_count = Column(Integer)
    latency_ms = Column(Float)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
