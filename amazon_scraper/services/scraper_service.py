from amazon_scraper.scraper import AmazonScraper
from amazon_scraper.selectors.selector_loader import SelectorLoader

class ScraperService:
    def __init__(self, browser_manager):
        selectors = SelectorLoader.load_selectors()
        self.scraper = AmazonScraper(browser_manager, selectors)

    async def scrape_products(self, query: str):
        products = await self.scraper.scrape(query)
        return products
