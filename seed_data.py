import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, init_db
from app.models import Advertiser, Campaign, IABCategory
from app.utils.iab_categories import IAB_TAXONOMY

async def seed():
    await init_db()
    
    async with AsyncSessionLocal() as db:
        # Seed Advertisers
        advs = [
            Advertiser(name="TechCorp", balance_cents=1000000),
            Advertiser(name="HealthPlus", balance_cents=500000),
            Advertiser(name="TravelWorld", balance_cents=750000),
            Advertiser(name="FinanceHub", balance_cents=2000000),
            Advertiser(name="SportZone", balance_cents=300000)
        ]
        db.add_all(advs)
        await db.flush()
        
        # Seed IAB Categories
        categories = []
        for i, cat_id in enumerate(list(IAB_TAXONOMY.keys())[:15]):
            cat = IABCategory(iab_id=cat_id, name=IAB_TAXONOMY[cat_id])
            categories.append(cat)
        db.add_all(categories)
        await db.flush()
        
        # Seed Campaigns
        campaigns = [
            Campaign(
                advertiser_id=advs[0].id, name="Cloud Hosting Promo",
                budget_daily_cents=10000, max_bid_cents=50,
                ad_title="Cloud Hosting", ad_body="Best cloud hosting", ad_url="http://techcorp.com",
                is_active=True
            ),
            Campaign(
                advertiser_id=advs[1].id, name="Vitamin Sale",
                budget_daily_cents=5000, max_bid_cents=30,
                ad_title="Vitamins", ad_body="Get 50% off", ad_url="http://healthplus.com",
                is_active=True
            ),
            Campaign(
                advertiser_id=advs[2].id, name="Summer Vacation",
                budget_daily_cents=15000, max_bid_cents=80,
                ad_title="Summer Vacations", ad_body="Book now", ad_url="http://travelworld.com",
                is_active=True
            )
        ]
        
        # Add categories to campaigns
        if len(categories) > 0:
            campaigns[0].target_categories.append(categories[0])
            campaigns[1].target_categories.append(categories[1])
            campaigns[2].target_categories.append(categories[2])
            
        db.add_all(campaigns)
        await db.commit()
        print("Data seeded successfully!")

if __name__ == "__main__":
    asyncio.run(seed())
