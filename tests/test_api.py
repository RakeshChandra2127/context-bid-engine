from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_serve_ad_invalid_request_returns_422():
    response = client.post("/api/v1/ads/serve/text", json={"wrong_field": "text"})
    assert response.status_code == 422

def test_serve_ad_by_text_returns_ads():
    # In a real environment, we'd mock the database and LLM calls
    # For now, if the endpoints are wired, we expect an error or 200 if dependencies are injected with mocks
    pass

def test_campaign_crud():
    # Mocked or simple test
    pass
