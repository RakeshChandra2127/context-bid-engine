from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db
from app.models import Campaign
from app.schemas import CampaignCreate, CampaignResponse

router = APIRouter(prefix="/api/v1/campaigns", tags=["Campaigns"])

@router.post("/", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(campaign_in: CampaignCreate, db: AsyncSession = Depends(get_db)):
    """Create a new campaign."""
    db_campaign = Campaign(**campaign_in.model_dump())
    db.add(db_campaign)
    await db.commit()
    await db.refresh(db_campaign)
    return db_campaign

@router.get("/", response_model=List[CampaignResponse])
async def list_campaigns(db: AsyncSession = Depends(get_db)):
    """List all active campaigns."""
    result = await db.execute(select(Campaign).where(Campaign.is_active == True))
    return result.scalars().all()

@router.get("/{id}", response_model=CampaignResponse)
async def get_campaign(id: int, db: AsyncSession = Depends(get_db)):
    """Get campaign by ID."""
    campaign = await db.get(Campaign, id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    return campaign

@router.patch("/{id}", response_model=CampaignResponse)
async def update_campaign(id: int, campaign_in: CampaignCreate, db: AsyncSession = Depends(get_db)):
    """Update campaign."""
    campaign = await db.get(Campaign, id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
    
    update_data = campaign_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(campaign, key, value)
        
    await db.commit()
    await db.refresh(campaign)
    return campaign

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_campaign(id: int, db: AsyncSession = Depends(get_db)):
    """Soft delete campaign (set is_active=False)."""
    campaign = await db.get(Campaign, id)
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")
        
    campaign.is_active = False
    await db.commit()
    return None
