# scraper.py (refatorado para usar BrowserManager)

import json
import os
from datetime import datetime
from typing import List, Optional

from loguru import logger

from amazon_scraper.model import Product
from amazon_scraper.selector_loader import SelectorLoader
from amazon_scraper.utils import async_retry
from amazon_scraper.core.browser_manager import BrowserManager


class AmazonScraper:
    def __init__(self, browser_manager: Optional[BrowserManager] = None):
        self.browser_manager = browser_manager or BrowserManager()
        self.selectors = SelectorLoader.load_selectors()

    async def init_browser(self):
        await self.browser_manager.start_browser(headless=False)

    async def close(self):
        await self.browser_manager.close_browser()

    @async_retry(retries=3, delay=2)
    async def scrape(self, query: str) -> List[Product]:
        page = self.browser_manager.get_page()
        search_url = self.selectors['search_url_template'].format(query=query)
        logger.info(f"Navigating to {search_url}")

        await page.goto(search_url, timeout=60000)

        os.makedirs("output/screenshots", exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        await page.screenshot(path=f"output/screenshots/screenshot_{query}_{timestamp}.png", full_page=True)

        html_content = await page.content()
        with open(f"output/page_source_{query}_{timestamp}.html", "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info(f"Saved page HTML to output/page_source_{query}_{timestamp}.html")

        await page.wait_for_selector(self.selectors['product_block'][0], timeout=30000)
        await page.wait_for_function(self.selectors['wait_for_products_function'], timeout=30000)


        products = []
        product_elements = await page.query_selector_all(self.selectors['product_block'][0])

        for element in product_elements:
            title = await self.extract_text(element, self.selectors['title'])
            price = await self.extract_text(element, self.selectors['price'])
            rating = await self.extract_text(element, self.selectors['rating'])
            reviews = await self.extract_text(element, self.selectors['reviews'])
            link = await self.extract_attribute(element, self.selectors['link'], "href")
            image_url = await self.extract_attribute(element, self.selectors['image_url'], "src")
            delivery = await self.extract_text(element, self.selectors['delivery'])
            badge = await self.extract_text(element, self.selectors['badge'])

            if title:
                products.append(Product(
                    title=title, price=price, rating=rating, reviews=reviews,
                    link=link, image_url=image_url, delivery=delivery, badge=badge
                ))

        logger.info(f"Scraped {len(products)} products.")

        if products:
            output_file = f"output/products_{query}_{timestamp}.json"
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump([product.model_dump() for product in products], f, ensure_ascii=False, indent=2)
            logger.info(f"Saved products to {output_file}")

        return products

    @staticmethod
    async def extract_text(element, selectors: List[str]) -> Optional[str]:
        for selector in selectors:
            try:
                sub_element = await element.query_selector(selector)
                if sub_element:
                    text = await sub_element.inner_text()
                    if text:
                        return text.strip()
            except Exception as e:
                logger.warning(f"Failed to extract with selector {selector}: {e}")
        return None

    @staticmethod
    async def extract_attribute(element, selectors: List[str], attribute: str) -> Optional[str]:
        for selector in selectors:
            try:
                sub_element = await element.query_selector(selector)
                if sub_element:
                    attr_value = await sub_element.get_attribute(attribute)
                    if attr_value:
                        return attr_value.strip()
            except Exception as e:
                logger.warning(f"Failed to extract attribute {attribute} with selector {selector}: {e}")
        return None
