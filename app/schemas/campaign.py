from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel

class CampaignBase(BaseModel):
    """Campaign base schema."""
    name: str
    ad_title: str
    ad_description: str
    ad_url: str
    bid_amount_cents: int
    daily_budget_cents: int

class CampaignCreate(CampaignBase):
    """Campaign creation schema."""
    target_category_codes: List[str]

class CampaignUpdate(BaseModel):
    """Campaign update schema."""
    name: Optional[str] = None
    ad_title: Optional[str] = None
    ad_description: Optional[str] = None
    ad_url: Optional[str] = None
    bid_amount_cents: Optional[int] = None
    daily_budget_cents: Optional[int] = None
    is_active: Optional[bool] = None
    target_category_codes: Optional[List[str]] = None

class CampaignResponse(CampaignBase):
    """Campaign response schema."""
    id: int
    advertiser_id: int
    advertiser_name: str
    spent_today_cents: int
    is_active: bool
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    target_category_codes: List[str]

    model_config = {"from_attributes": True}
