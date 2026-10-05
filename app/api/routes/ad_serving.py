from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from app.schemas import AdRequestByURL, AdRequestByText, AdResponse, ErrorResponse
from app.services.ad_selector import AdSelector
from app.api.dependencies import get_ad_selector, get_cache_service
from app.services.cache_service import CacheService

router = APIRouter(prefix="/api/v1/ads", tags=["Ad Serving"])

@router.post(
    "/serve/url",
    response_model=AdResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Serve ads for a given URL"
)
async def serve_ads_by_url(
    request: AdRequestByURL,
    ad_selector: AdSelector = Depends(get_ad_selector)
):
    """
    Fetches the content from the provided URL, analyzes it using an LLM to determine
    the contextual IAB categories, runs a real-time second-price auction among eligible
    campaigns, and returns the winning ads.
    """
    try:
        response = await ad_selector.serve_ads_for_url(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post(
    "/serve/text",
    response_model=AdResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Serve ads for raw text"
)
async def serve_ads_by_text(
    request: AdRequestByText,
    ad_selector: AdSelector = Depends(get_ad_selector)
):
    """
    Analyzes the provided text directly to determine contextual IAB categories,
    runs a real-time second-price auction, and returns the winning ads.
    """
    try:
        response = await ad_selector.serve_ads_for_text(request)
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/auction-log",
    summary="Get recent auction logs"
)
async def get_auction_log(ad_selector: AdSelector = Depends(get_ad_selector)):
    """
    Returns the 50 most recent auction logs for monitoring and debugging.
    """
    try:
        logs = await ad_selector.get_recent_auction_logs(limit=50)
        return logs
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get(
    "/cache-stats",
    summary="Get cache statistics"
)
async def get_cache_stats(cache_service: CacheService = Depends(get_cache_service)):
    """
    Returns Redis cache hit/miss statistics.
    """
    try:
        stats = await cache_service.get_stats()
        return stats
    except Exception as e:
         raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
