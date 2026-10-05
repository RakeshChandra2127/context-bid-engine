from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import Advertiser
from app.schemas import AdvertiserCreate, AdvertiserResponse

router = APIRouter(prefix="/api/v1/advertisers", tags=["Advertisers"])

@router.post("/", response_model=AdvertiserResponse, status_code=status.HTTP_201_CREATED)
async def create_advertiser(advertiser_in: AdvertiserCreate, db: AsyncSession = Depends(get_db)):
    """Create a new advertiser."""
    db_advertiser = Advertiser(**advertiser_in.model_dump())
    db.add(db_advertiser)
    await db.commit()
    await db.refresh(db_advertiser)
    return db_advertiser

@router.get("/", response_model=List[AdvertiserResponse])
async def list_advertisers(db: AsyncSession = Depends(get_db)):
    """List all advertisers."""
    result = await db.execute(select(Advertiser))
    return result.scalars().all()

@router.get("/{id}", response_model=AdvertiserResponse)
async def get_advertiser(id: int, db: AsyncSession = Depends(get_db)):
    """Get advertiser by ID with campaigns."""
    result = await db.execute(
        select(Advertiser)
        .options(selectinload(Advertiser.campaigns))
        .where(Advertiser.id == id)
    )
    advertiser = result.scalar_one_or_none()
    
    if not advertiser:
        raise HTTPException(status_code=404, detail="Advertiser not found")
    return advertiser
