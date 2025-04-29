import pytest
import asyncio
from amazon_scraper.core.page_saver import PageSaver

class DummyPage:
    def __init__(self, html):
        self._html = html
    async def content(self):
        return self._html
    async def screenshot(self, path, full_page=True):
        # simula criação do arquivo
        with open(path, "wb") as f:
            f.write(b"PNGDATA")

@pytest.mark.asyncio
async def test_save_html(tmp_path):
    page = DummyPage("<html>ok</html>")
    out = await PageSaver.save_html(page, "q", base_path=str(tmp_path/"o"))
    assert (tmp_path/"o"/"pages").exists()
    assert out.endswith(".html")
    assert "ok" in open(out, encoding="utf-8").read()

@pytest.mark.asyncio
async def test_save_screenshot(tmp_path):
    page = DummyPage("")
    out = await PageSaver.save_screenshot(page, "q", base_path=str(tmp_path/"o"))
    assert (tmp_path/"o"/"screenshots").exists()
    assert out.endswith(".png")
    # arquivo não vazio
    assert (tmp_path/"o"/"screenshots"/out.split("/")[-1]).stat().st_size > 0
