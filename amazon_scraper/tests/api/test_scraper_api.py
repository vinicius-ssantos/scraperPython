import pytest
from fastapi.testclient import TestClient
from amazon_scraper.api.scraper_api import app
from amazon_scraper.api.router import get_scraper_service
from amazon_scraper.models.product import Product

class DummyService:
    async def scrape(self, query):
        return [Product(title="T", price="P")]

@pytest.fixture(autouse=True)
def override_service(monkeypatch):
    async def _get():
        yield DummyService()
    monkeypatch.setattr("amazon_scraper.api.router.get_scraper_service", _get)

def test_scrape_endpoint():
    client = TestClient(app)
    r = client.get("/api/scrape?query=foo")
    assert r.status_code == 200
    body = r.json()
    assert "products" in body
    assert body["products"][0]["title"] == "T"
