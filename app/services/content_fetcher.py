import hashlib
import logging
from bs4 import BeautifulSoup
import httpx

logger = logging.getLogger(__name__)

class ContentFetcher:
    def __init__(self, timeout_seconds: int = 5):
        self.timeout_seconds = timeout_seconds

    async def fetch_page_content(self, url: str) -> str:
        try:
            async with httpx.AsyncClient(timeout=self.timeout_seconds) as client:
                response = await client.get(url, follow_redirects=True)
                response.raise_for_status()
                
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Remove script and style elements
            for script_or_style in soup(["script", "style", "noscript"]):
                script_or_style.extract()
                
            # Extract meaningful text
            elements = soup.find_all(['title', 'meta', 'h1', 'h2', 'h3', 'p'])
            text_parts = []
            
            for elem in elements:
                if elem.name == 'meta':
                    if elem.get('name', '').lower() == 'description':
                        content = elem.get('content')
                        if content:
                            text_parts.append(content)
                else:
                    text = elem.get_text(separator=' ', strip=True)
                    if text:
                        text_parts.append(text)
                        
            # Also get remaining text just in case
            if not text_parts:
                text = soup.get_text(separator=' ', strip=True)
                text_parts.append(text)
                
            combined_text = " ".join(text_parts)
            
            # Limit to 5000 characters
            return combined_text[:5000]
            
        except httpx.TimeoutException:
            logger.error(f"Timeout while fetching URL: {url}")
            return ""
        except Exception as e:
            logger.error(f"Error fetching URL {url}: {e}")
            return ""

    def compute_content_hash(self, content: str) -> str:
        return hashlib.sha256(content.encode("utf-8")).hexdigest()
