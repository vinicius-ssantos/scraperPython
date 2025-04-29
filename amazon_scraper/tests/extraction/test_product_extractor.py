import pytest
from amazon_scraper.extraction.product_extractor import ProductExtractor
from amazon_scraper.core.fallback_selector_resolver import FallbackSelectorResolver
from amazon_scraper.models.product import Product

class DummyElement:
    def __init__(self, data):
        self.data = data
    async def query_selector(self, selector):
        class Sub:
            def __init__(self, text=None, attr=None):
                self._text = text
                self._attr = attr
            async def inner_text(self):
                return self._text
            async def get_attribute(self, name):
                return self._attr
        val = self.data.get(selector)
        if not val:
            return None
        if isinstance(val, tuple):
            return Sub(text=val[0], attr=val[1])
        return Sub(text=val)

@pytest.mark.asyncio
async def test_extract_product_all_fields():
    selectors = {
        "title": ["t"],
        "price": ["p"],
        "rating": ["r"],
        "reviews": ["v"],
        "link": ["l"],
        "image_url": ["i"],
        "delivery": ["d"],
        "badge": ["b"]
    }
    values = {
        "t": "MyTitle",
        "p": "R$100",
        "r": "5 estrelas",
        "v": "10 avaliações",
        "l": ("", "http://link"),
        "i": ("", "http://img"),
        "d": "Entrega grátis",
        "b": "Mais vendidos"
    }
    elem = DummyElement(values)
    extractor = ProductExtractor(selectors)
    product = await extractor.extract_product(elem)
    assert isinstance(product, Product)
    assert product.title == "MyTitle"
    assert product.link == "http://link"
    assert product.image_url == "http://img"
