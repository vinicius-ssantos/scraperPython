# amazon_scraper/main.py

import asyncio
from amazon_scraper import AmazonScraper
from amazon_scraper.selectors.selector_loader import SelectorLoader
from loguru import logger

async def main():
    selectors = SelectorLoader.load_selectors()
    query = selectors.get("query", "ssd")  # busca a palavra-chave, fallback para "ssd"

    scraper = AmazonScraper()
    await scraper.init_browser()
    products = await scraper.scrape(query)

    for product in products:
        logger.info(product.model_dump())

    await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())
