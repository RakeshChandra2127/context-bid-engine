from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class IABCategory(Base):
    """IAB Category model."""

    __tablename__ = "category"

    id = Column(Integer, primary_key=True)
    code = Column(String(20), nullable=False, unique=True)
    name = Column(String(255), nullable=False)
    parent_code = Column(String(20), nullable=True)

    campaigns = relationship(
        "Campaign", secondary="campaign_categories", back_populates="target_categories"
    )
