import json
import logging
from typing import Dict, Any
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

from app.schemas import ContentAnalysis
from app.config import get_settings

logger = logging.getLogger(__name__)

class ContentAnalyzerError(Exception):
    pass

class ContentAnalyzer:
    def __init__(self):
        self.settings = get_settings()
        self.provider = self.settings.AI_PROVIDER.lower()
        self.model = self.settings.AI_MODEL
        self.timeout = self.settings.AI_TIMEOUT_SECONDS
        
        if self.provider == "openai":
            self.client = AsyncOpenAI(api_key=self.settings.OPENAI_API_KEY, timeout=self.timeout)
        elif self.provider == "anthropic":
            self.client = AsyncAnthropic(api_key=self.settings.ANTHROPIC_API_KEY, timeout=self.timeout)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")

    def _build_prompt(self, text: str) -> str:
        return f"""
        You are an advanced text classification system. Your task is to analyze the following content and categorize it according to the IAB (Interactive Advertising Bureau) taxonomy.
        
        Content to analyze:
        ---
        {text}
        ---
        
        Instructions:
        1. Identify 1-3 IAB categories that best describe the content.
        2. Extract 3-8 key topics or keywords.
        3. Identify the single most relevant primary IAB category code.
        
        Output MUST be valid JSON with the following structure:
        {{
            "categories": [
                {{"code": "IAB1", "name": "Arts & Entertainment", "confidence": 0.95}},
                {{"code": "IAB1-1", "name": "Books & Literature", "confidence": 0.8}}
            ],
            "topics": ["keyword1", "keyword2", "keyword3"],
            "primary_category": "IAB1"
        }}
        
        Ensure confidence scores are between 0.0 and 1.0. ONLY output JSON.
        """

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(Exception)
    )
    async def analyze_content(self, text: str) -> ContentAnalysis:
        truncated_text = text[:3000]
        prompt = self._build_prompt(truncated_text)
        
        try:
            if self.provider == "openai":
                result = await self._analyze_with_openai(prompt)
            else:
                result = await self._analyze_with_anthropic(prompt)
                
            return ContentAnalysis(**result)
            
        except Exception as e:
            logger.error(f"Error during content analysis: {e}")
            raise ContentAnalyzerError(f"Failed to analyze content: {e}")

    async def _analyze_with_openai(self, prompt: str) -> Dict[str, Any]:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that outputs ONLY valid JSON."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1
        )
        
        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from OpenAI")
            
        return json.loads(content)

    async def _analyze_with_anthropic(self, prompt: str) -> Dict[str, Any]:
        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            temperature=0.1,
            system="You are a JSON-only response bot. Only return valid JSON.",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        content = response.content[0].text
        if not content:
            raise ValueError("Empty response from Anthropic")
            
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Fallback for Anthropic if it includes markdown JSON block
            import re
            json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group(1))
            raise
