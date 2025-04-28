# amazon_scraper/api/router.py

from fastapi import APIRouter, Depends
from amazon_scraper.core.browser_manager import BrowserManager
from amazon_scraper.services.scraper_service import AmazonScraperService
from amazon_scraper.scraper_selectors.selector_loader import SelectorLoader

router = APIRouter()

# Dependência para gerenciar o ciclo de vida
async def get_scraper_service():
    browser_manager = BrowserManager()
    selectors = SelectorLoader.load_selectors()
    await browser_manager.start(headless=True)
    service = AmazonScraperService(browser_manager, selectors)
    try:
        yield service
    finally:
        await browser_manager.close()

@router.get("/scrape")
async def scrape_endpoint(query: str, scraper_service: AmazonScraperService = Depends(get_scraper_service)):
    products = await scraper_service.scrape(query)
    return {"products": [product.model_dump() for product in products]}