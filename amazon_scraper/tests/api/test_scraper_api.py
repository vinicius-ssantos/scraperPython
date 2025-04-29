import pytest
from fastapi.testclient import TestClient
from amazon_scraper.api.scraper_api import app
from amazon_scraper.api.router import get_scraper_service
from amazon_scraper.models.product import Product

class DummyService:
    async def scrape(self, query):
        # Retorna um produto dummy para teste
        return [Product(title="T", price="P")]

@pytest.fixture(autouse=True)
def override_dependency():
    # Substitui a dependência get_scraper_service pelo stub
    async def get_dummy_service():
        yield DummyService()
    app.dependency_overrides[get_scraper_service] = get_dummy_service
    yield
    # Limpa overrides após o teste
    app.dependency_overrides.clear()

def test_scrape_endpoint():
    client = TestClient(app)
    response = client.get("/api/scrape?query=foo")
    assert response.status_code == 200
    body = response.json()
    assert "products" in body
    assert isinstance(body["products"], list)
    assert body["products"][0]["title"] == "T"
