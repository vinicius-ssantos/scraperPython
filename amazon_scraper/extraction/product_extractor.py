# extraction/product_extractor.py

from amazon_scraper.core.fallback_selector_resolver import FallbackSelectorResolver
from amazon_scraper.models.product import Product


class ProductExtractor:
    def __init__(self, selectors: dict):
        self.selectors = selectors

    async def extract_product(self, element) -> Product:
        title = await FallbackSelectorResolver.resolve_text(element, self.selectors['title'])
        price = await FallbackSelectorResolver.resolve_text(element, self.selectors['price'])
        rating = await FallbackSelectorResolver.resolve_text(element, self.selectors['rating'])
        reviews = await FallbackSelectorResolver.resolve_text(element, self.selectors['reviews'])
        link = await FallbackSelectorResolver.resolve_attribute(element, self.selectors['link'], "href")
        image_url = await FallbackSelectorResolver.resolve_attribute(element, self.selectors['image_url'], "src")
        delivery = await FallbackSelectorResolver.resolve_text(element, self.selectors['delivery'])
        badge = await FallbackSelectorResolver.resolve_text(element, self.selectors['badge'])

        return Product(
            title=title, price=price, rating=rating, reviews=reviews,
            link=link, image_url=image_url, delivery=delivery, badge=badge
        )

