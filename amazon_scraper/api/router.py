# amazon_scraper/api/router.py
from fastapi import APIRouter, Query
from amazon_scraper.services.scraper_service import ScraperService
from amazon_scraper.core.browser_manager import BrowserManager
from amazon_scraper.selectors.selector_loader import SelectorLoader

router = APIRouter()
scraper_service = ScraperService(BrowserManager())

@router.get("/scrape")
async def scrape_endpoint(query: str = Query(..., description="Search query for Amazon")):
    await scraper_service.scraper.browser_manager.start_browser(headless=False)  # 🛠️ inicializa o browser
    products = await scraper_service.scrape_products(query)
    await scraper_service.scraper.browser_manager.close_browser()  # 🛠️ fecha depois

    return {"products": [product.model_dump() for product in products]}
