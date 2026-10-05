from pydantic import BaseModel, Field, HttpUrl

class AdRequestByURL(BaseModel):
    """Ad request by URL."""
    url: HttpUrl
    max_ads: int = Field(default=1, le=10)

class AdRequestByText(BaseModel):
    """Ad request by text content."""
    text: str = Field(min_length=50, max_length=50000)
    max_ads: int = Field(default=1)
