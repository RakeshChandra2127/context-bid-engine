from typing import List, Optional
from pydantic import BaseModel

class ServedAd(BaseModel):
    """Ad served in response."""
    campaign_id: int
    ad_title: str
    ad_description: str
    ad_url: str
    advertiser_name: str
    relevance_score: float
    clearing_price_cents: Optional[int] = None

class CategoryConfidence(BaseModel):
    """Category confidence."""
    code: str
    name: str
    confidence: float

class ContentAnalysis(BaseModel):
    """Content analysis result."""
    categories: List[CategoryConfidence]
    topics: List[str]
    primary_category: str

class AdResponse(BaseModel):
    """Ad response."""
    request_id: str
    ads: List[ServedAd]
    content_analysis: ContentAnalysis
    candidates_evaluated: int
    latency_ms: float
    cached: bool

class ErrorResponse(BaseModel):
    """Error response."""
    detail: str
    error_code: str
