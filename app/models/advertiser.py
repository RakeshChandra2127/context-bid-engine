from datetime import datetime

from sqlalchemy import BigInteger, Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Advertiser(Base):
    """Advertiser model."""

    __tablename__ = "advertiser"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    industry = Column(String(100))
    budget_cents = Column(BigInteger, nullable=False, default=0)
    is_active = Column(Boolean, default=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    campaigns = relationship(
        "Campaign", back_populates="advertiser", cascade="all, delete-orphan"
    )
