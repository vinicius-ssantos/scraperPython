import pytest
import asyncio
from amazon_scraper.core.fallback_selector_resolver import FallbackSelectorResolver

class DummyElement:
    def __init__(self, results):
        # results: dict selector -> value
        self._results = results

    async def query_selector(self, selector):
        class Sub:
            def __init__(self, text=None, attr=None):
                self._text = text
                self._attr = attr
            async def inner_text(self):
                return self._text
            async def get_attribute(self, name):
                return self._attr
        if selector in self._results:
            val = self._results[selector]
            if isinstance(val, tuple):
                return Sub(text=val[0], attr=val[1])
            else:
                return Sub(text=val)
        return None

@pytest.mark.asyncio
async def test_resolve_text_first_match():
    elem = DummyElement({
        "sel1": None,
        "sel2": "  Hello  ",
        "sel3": "Ignored"
    })
    text = await FallbackSelectorResolver.resolve_text(elem, ["sel1", "sel2", "sel3"])
    assert text == "Hello"

@pytest.mark.asyncio
async def test_resolve_text_no_match():
    elem = DummyElement({})
    text = await FallbackSelectorResolver.resolve_text(elem, ["a", "b"])
    assert text is None

@pytest.mark.asyncio
async def test_resolve_attribute():
    elem = DummyElement({
        "link": ("", "http://foo"),
        "other": None
    })
    url = await FallbackSelectorResolver.resolve_attribute(elem, ["other", "link"], "href")
    assert url == "http://foo"
