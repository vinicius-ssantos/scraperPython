from amazon_scraper.scraper import AmazonScraperService
from amazon_scraper.scraper_selectors.selector_loader import SelectorLoader

class ScraperService:
    def __init__(self, browser_manager):
        selectors = SelectorLoader.load_selectors()
        self.scraper = AmazonScraperService(browser_manager, selectors)

    async def scrape_products(self, query: str):
        products = await self.scraper.scrape(query)
        return products
