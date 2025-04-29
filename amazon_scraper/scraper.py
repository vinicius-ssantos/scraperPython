# amazon_scraper/scraper.py

# Continuação da refatoração seguindo SOLID e boas práticas:
from amazon_scraper.core.browser_session import BrowserSession
from amazon_scraper.scraper_selectors.selector_loader import SelectorLoader
from amazon_scraper.extraction.product_extractor import ProductExtractor
from amazon_scraper.core.page_saver import PageSaver
from amazon_scraper.utils.async_retry import async_retry
import json
import os
from datetime import datetime
from amazon_scraper.models.product import Product
from loguru import logger

class AmazonScraperService:
    def __init__(self, browser_session: BrowserSession, selectors: dict = None):
        self.browser_session = browser_session
        self.selectors = selectors or SelectorLoader.load_selectors()
        self.product_extractor = ProductExtractor(self.selectors)

    @async_retry(retries=3, base_delay=2)
    async def scrape(self, query: str) -> list[Product]:
        page = self.browser_session.get_page()
        search_url = self.selectors['search_url_template'].format(query=query)
        logger.info(f"Navegando para {search_url}")

        await page.goto(search_url, timeout=60000)

        # Faz fallback de base_path usando variável de ambiente
        base = os.getenv("OUTPUT_BASE_PATH", "output")

        # Salvando página HTML e screenshot (podem ser stubs em testes)
        await PageSaver.save_html(page, query, base_path=base)
        await PageSaver.save_screenshot(page, query, base_path=base)

        await page.wait_for_selector(self.selectors['product_block'][0], timeout=30000)
        await page.wait_for_function(self.selectors['wait_for_products_function'], timeout=30000)

        product_elements = await page.query_selector_all(self.selectors['product_block'][0])
        products: list[Product] = []

        for element in product_elements:
            try:
                product = await self.product_extractor.extract_product(element)
                if product.title:
                    products.append(product)
            except Exception as e:
                logger.warning(f"Falha ao extrair produto: {e}")

        logger.info(f"Total de produtos extraídos: {len(products)}")

        # Salva JSON se houver produtos
        if products:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            products_dir = os.path.join(base, "products")
            os.makedirs(products_dir, exist_ok=True)

            output_file = os.path.join(
                products_dir,
                f"products_{query}_{timestamp}.json"
            )
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump([p.model_dump() for p in products], f, ensure_ascii=False, indent=2)

            logger.info(f"Produtos salvos em {output_file}")

        return products
