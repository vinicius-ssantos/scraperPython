import pytest
import asyncio
import json
import os
from amazon_scraper.services.scraper_service import ScraperService
from amazon_scraper.core.browser_manager import BrowserManager
from amazon_scraper.core.page_saver import PageSaver

class DummyPage:
    def __init__(self, elements):
        self._elements = elements
    async def goto(self, url, timeout=None):
        pass
    async def wait_for_selector(self, sel, timeout=None):
        pass
    async def wait_for_function(self, func, timeout=None):
        pass
    async def query_selector_all(self, sel):
        return self._elements

class DummySession:
    def __init__(self, page):
        self._page = page
    def get_page(self):
        return self._page

@pytest.mark.asyncio
async def test_scrape_no_products(monkeypatch, tmp_path):
    # Stubs para PageSaver evitar chamar page.content() e screenshot()
    async def dummy_save_html(page, query, base_path="output"):
        return ""
    async def dummy_save_screenshot(page, query, base_path="output"):
        return ""
    monkeypatch.setattr(PageSaver, 'save_html', dummy_save_html)
    monkeypatch.setattr(PageSaver, 'save_screenshot', dummy_save_screenshot)

    # página sem produtos
    page = DummyPage([])
    session = DummySession(page)
    svc = ScraperService(session)
    products = await svc.scraper.scrape("q")
    assert products == []

@pytest.mark.asyncio
async def test_scrape_and_save(monkeypatch, tmp_path):
    # Stubs para PageSaver
    async def dummy_save_html(page, query, base_path="output"):
        return ""
    async def dummy_save_screenshot(page, query, base_path="output"):
        return ""
    monkeypatch.setattr(PageSaver, 'save_html', dummy_save_html)
    monkeypatch.setattr(PageSaver, 'save_screenshot', dummy_save_screenshot)

    # cria um elemento que rende um produto
    class Elem:
        async def query_selector(self, sel):
            class Sub:
                async def inner_text(self): return "X"
                async def get_attribute(self, a): return "Y"
            return Sub()

    page = DummyPage([Elem()])
    session = DummySession(page)
    svc = ScraperService(session)
    # força output em tmp_path
    monkeypatch.setenv("OUTPUT_BASE_PATH", str(tmp_path/"o"))
    products = await svc.scraper.scrape("q")
    # confirma saída de produto
    assert len(products) == 1
    assert products[0].title == "X"
    # verifica arquivo JSON gerado
    out_dir = tmp_path/"o"/"products"
    files = list(out_dir.glob("*.json"))
    assert len(files) == 1
    data = json.load(open(files[0], encoding="utf-8"))
    assert isinstance(data, list) and data[0]["title"] == "X"
