import asyncio
from amazon_scraper.services.scraper_service import ScraperService
from amazon_scraper.core.browser_manager import BrowserManager
from amazon_scraper.scraper_selectors.selector_loader import SelectorLoader

async def run_cli():
    selectors = SelectorLoader.load_selectors()
    browser_manager = BrowserManager()
    await browser_manager.start_browser(headless=False)

    scraper_service = ScraperService(browser_manager)
    query = selectors.get("query", "ssd")
    products = await scraper_service.scrape_products(query)

    for product in products:
        print(product.model_dump())

    await browser_manager.close_browser()

if __name__ == "__main__":
    asyncio.run(run_cli())
