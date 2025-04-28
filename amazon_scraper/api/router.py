# amazon_scraper/api/router.py
from fastapi import APIRouter, Query
from amazon_scraper.services.scraper_service import ScraperService
from amazon_scraper.core.browser_manager import BrowserManager
from amazon_scraper.utils.selector_loader import SelectorLoader

router = APIRouter()
scraper_service = ScraperService(BrowserManager(), SelectorLoader())

@router.get("/scrape")
async def scrape_endpoint(query: str = Query(..., description="Search query for Amazon")):
    products = scraper_service.scrape_products(query)
    return {"products": products}