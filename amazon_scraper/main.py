import asyncio
from amazon_scraper.core.browser_manager import BrowserManager
from amazon_scraper.services.scraper_service import AmazonScraperService
from amazon_scraper.scraper_selectors.selector_loader import SelectorLoader
from loguru import logger

async def main():
    selectors = SelectorLoader.load_selectors()
    browser_manager = BrowserManager()

    await browser_manager.start(headless=False)
    scraper_service = AmazonScraperService(browser_manager, selectors)

    query = selectors.get("query", "ssd")
    products = await scraper_service.scrape(query)

    for product in products:
        logger.info(product.model_dump())

    await browser_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
