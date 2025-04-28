# amazon_scraper/main.py

import asyncio
from amazon_scraper import AmazonScraper
from loguru import logger

async def main():
    query = "ssd"
    scraper = AmazonScraper()
    products = await scraper.scrape(query)

    for product in products:
        logger.info(product.model_dump())

    await scraper.close()

if __name__ == "__main__":
    asyncio.run(main())
