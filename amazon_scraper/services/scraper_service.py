# amazon_scraper/services/scraper_service.py
from amazon_scraper.scraper import AmazonScraper

class ScraperService:
    def __init__(self, browser_manager, selectors_loader):
        self.scraper = AmazonScraper(browser_manager, selectors_loader)

    def scrape_products(self, query: str):
        return self.scraper.scrape(query)