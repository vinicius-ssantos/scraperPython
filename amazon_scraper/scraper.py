# amazon_scraper/scraper.py

import json
import os
from datetime import datetime
from typing import Optional

from loguru import logger
from playwright.async_api import async_playwright, Browser, Page

from model import Product
from selector_loader import SelectorLoader
from utils import async_retry

class AmazonScraper:
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None
        self.selectors = SelectorLoader.load_selectors()

    async def init_browser(self):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=False)
        self.page = await self.browser.new_page()

    async def close(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    @async_retry(retries=3, delay=2)
    async def scrape(self, query: str) -> list[Product]:
        if not self.browser:
            await self.init_browser()

        search_url = f"https://www.amazon.com.br/s?k={query}"
        logger.info(f"Navigating to {search_url}")
        await self.page.goto(search_url, timeout=60000)

        # Gera timestamp único
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        # Cria pasta para a execução
        output_dir = os.path.join("output", f"{query}_{timestamp}")
        os.makedirs(output_dir, exist_ok=True)

        # Screenshot
        screenshot_path = os.path.join(output_dir, "screenshot.png")
        await self.page.screenshot(path=screenshot_path, full_page=True)
        logger.info(f"Saved screenshot to {screenshot_path}")

        # HTML da página
        html_content = await self.page.content()
        html_file_path = os.path.join(output_dir, "page_source.html")
        with open(html_file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info(f"Saved page HTML to {html_file_path}")

        # Espera produtos renderizarem
        await self.page.wait_for_function(
            """() => document.querySelectorAll("div.s-result-item[data-asin]:not([data-asin=''])").length > 20""",
            timeout=30000
        )

        products = []
        product_elements = await self.page.query_selector_all(self.selectors['product_block'][0])

        for element in product_elements:
            title = await self.extract_text(element, self.selectors['title'])
            price = await self.extract_text(element, self.selectors['price'])
            rating = await self.extract_text(element, self.selectors['rating'])
            reviews = await self.extract_text(element, self.selectors['reviews'])

            link_element = await element.query_selector(self.selectors['link'][0])
            image_element = await element.query_selector(self.selectors['image_url'][0])
            delivery = await self.extract_text(element, self.selectors['delivery'])
            badge = await self.extract_text(element, self.selectors['badge'])

            link = await link_element.get_attribute('href') if link_element else None
            image_url = await image_element.get_attribute('src') if image_element else None
            asin = await element.get_attribute('data-asin')

            if title:
                products.append(Product(
                    title=title,
                    price=price,
                    rating=rating,
                    reviews=reviews,
                    link=link,
                    image_url=image_url,
                    delivery=delivery,
                    badge=badge,
                    asin=asin
                ))

        logger.info(f"Scraped {len(products)} products.")

        if products:
            products_file = os.path.join(output_dir, "products.json")
            with open(products_file, "w", encoding="utf-8") as f:
                json.dump([product.model_dump() for product in products], f, ensure_ascii=False, indent=2)
            logger.info(f"Saved products to {products_file}")

        return products

    @staticmethod
    async def extract_text(element, selectors: list[str]) -> str | None:
        for selector in selectors:
            try:
                sub_element = await element.query_selector(selector)
                if sub_element:
                    # Primeiro tenta pegar inner_text (ideal para <span>, <div> etc.)
                    text = await sub_element.inner_text()
                    if text:
                        return text.strip()
                    # Se inner_text vazio, tenta pegar diretamente o atributo 'textContent'
                    text_content = await sub_element.get_attribute("textContent")
                    if text_content:
                        return text_content.strip()
            except Exception as e:
                logger.warning(f"Failed to extract with selector {selector}: {e}")
        return None

