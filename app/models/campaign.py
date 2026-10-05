from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Table,
    Text,
)
from sqlalchemy.orm import relationship

from app.database import Base

campaign_categories = Table(
    "campaign_categories",
    Base.metadata,
    Column("campaign_id", Integer, ForeignKey("campaign.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("category.id"), primary_key=True),
)


class Campaign(Base):
    """Campaign model."""

    __tablename__ = "campaign"

    id = Column(Integer, primary_key=True)
    advertiser_id = Column(Integer, ForeignKey("advertiser.id"), nullable=False)
    name = Column(String(255), nullable=False)
    ad_title = Column(String(200), nullable=False)
    ad_description = Column(Text, nullable=False)
    ad_url = Column(String(500), nullable=False)
    bid_amount_cents = Column(Integer, nullable=False)
    daily_budget_cents = Column(Integer, nullable=False)
    spent_today_cents = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True))

    advertiser = relationship("Advertiser", back_populates="campaigns")
    target_categories = relationship(
        "IABCategory", secondary=campaign_categories, back_populates="campaigns"
    )
