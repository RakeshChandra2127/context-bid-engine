import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import health, ad_serving, campaigns, advertisers
from app.database import init_db
from app.config import get_settings
from app.api.dependencies import get_redis_client

settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB tables
    await init_db()
    
    # Connect Redis cache
    redis = await get_redis_client()
    try:
        await redis.ping()
    except Exception as e:
        print(f"Failed to connect to Redis on startup: {e}")
        
    yield
    
    # Disconnect on shutdown
    await redis.close()

app = FastAPI(
    title="AdContext Engine - AI-Driven Contextual Ad Platform",
    description="Real-time contextual ad serving and bidding engine powered by LLMs",
    version=settings.version,
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response

# Include routers
app.include_router(health.router)
app.include_router(ad_serving.router)
app.include_router(campaigns.router)
app.include_router(advertisers.router)

@app.get("/", tags=["Root"])
async def root():
    return JSONResponse(content={
        "message": "Welcome to the AdContext Engine API",
        "docs_url": "/docs",
        "redoc_url": "/redoc",
        "version": settings.version
    })
