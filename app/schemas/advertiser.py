from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class AdvertiserBase(BaseModel):
    """Advertiser base schema."""
    name: str
    industry: Optional[str] = None
    budget_cents: int

class AdvertiserCreate(AdvertiserBase):
    """Advertiser creation schema."""
    pass

class AdvertiserResponse(AdvertiserBase):
    """Advertiser response schema."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = {"from_attributes": True}
