import pytest
import asyncio
import threading
from fastapi import FastAPI
from starlette.responses import FileResponse
from amazon_scraper.core.browser_manager import BrowserManager
from amazon_scraper.services.scraper_service import AmazonScraperService
from amazon_scraper.scraper_selectors.selector_loader import SelectorLoader

@pytest.fixture
# Fixture para iniciar um servidor HTTP local servindo um HTML de teste
# Usa tmp_path (scope de função), evitando pb de escopo
def http_server(tmp_path):
    # Salva um HTML simples em arquivo
    html = """
    <html><body>
      <div class=\"s-result-item\" data-asin=\"1\"> 
        <h2 class=\"a-spacing-none\"><span>Item1</span></h2>
      </div>
    </body></html>
    """
    f = tmp_path / "test.html"
    f.write_text(html, encoding="utf-8")

    app = FastAPI()
    @app.get("/test.html")
    def serve():
        return FileResponse(str(f))

    import uvicorn
    server_thread = threading.Thread(
        target=uvicorn.run,
        kwargs={
            "app": app,
            "host": "127.0.0.1",
            "port": 8002,
            "log_level": "critical"
        },
        daemon=True
    )
    server_thread.start()
    yield
    # Ao final do teste, o thread será finalizado junto com o processo de testes

@pytest.mark.asyncio
async def test_integration_scrape(http_server):
    # Ajusta selectors para apontar ao nosso servidor local
    SelectorLoader.load_selectors = staticmethod(lambda path=None: {
        "search_url_template": "http://127.0.0.1:8002/test.html",
        "product_block": ["div.s-result-item[data-asin]"],
        "wait_for_products_function": "() => true",
        "title": ["h2 span"],
        "price": [], "rating": [], "reviews": [],
        "link": [], "image_url": [], "delivery": [], "badge": []
    })

    manager = BrowserManager()
    await manager.start(headless=True)
    svc = AmazonScraperService(manager, SelectorLoader.load_selectors())
    products = await svc.scrape("anything")
    assert len(products) == 1
    assert products[0].title == "Item1"
    await manager.close()
