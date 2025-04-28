# amazon_scraper/run_cli.py
from amazon_scraper.services.scraper_service import ScraperService
from amazon_scraper.core.browser_manager import BrowserManager
from amazon_scraper.utils.selector_loader import SelectorLoader

if __name__ == "__main__":
    scraper_service = ScraperService(BrowserManager(), SelectorLoader())
    products = scraper_service.scrape_products("ssd")
    for product in products:
        print(product)