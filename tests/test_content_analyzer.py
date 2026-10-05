import pytest
from unittest.mock import patch, MagicMock
from app.services.content_analyzer import ContentAnalyzer

@pytest.mark.asyncio
async def test_build_prompt_includes_iab_categories():
    analyzer = ContentAnalyzer()
    prompt = analyzer._build_prompt("Some text content")
    assert "IAB" in prompt
    assert "Some text content" in prompt

def test_parse_valid_json_response():
    analyzer = ContentAnalyzer()
    valid_json = '{"categories": ["IAB1"], "sentiment": "neutral", "keywords": ["test"]}'
    res = analyzer._parse_response(valid_json)
    assert res.categories == ["IAB1"]
    assert res.sentiment == "neutral"

def test_parse_malformed_json_fallback():
    analyzer = ContentAnalyzer()
    malformed_json = '{"categories": ["IAB1", "sentiment": "neutral"'
    res = analyzer._parse_response(malformed_json)
    assert res.categories == []
    assert res.sentiment == "neutral"
    assert res.keywords == []

def test_truncates_long_content():
    analyzer = ContentAnalyzer()
    long_content = "a" * 10000
    truncated = analyzer._truncate_content(long_content, max_length=100)
    assert len(truncated) == 100
    assert truncated == "a" * 100

@pytest.mark.asyncio
@patch('app.services.content_analyzer.AsyncOpenAI')
async def test_analyze_text_mocked_llm(mock_openai):
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices[0].message.content = '{"categories": ["IAB1"], "sentiment": "neutral", "keywords": ["test"]}'
    mock_client.chat.completions.create.return_value = mock_response
    mock_openai.return_value = mock_client
    
    analyzer = ContentAnalyzer()
    analyzer.client = mock_client
    
    result = await analyzer.analyze_text("Some text")
    assert result.categories == ["IAB1"]
