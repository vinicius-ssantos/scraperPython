# core/browser_manager.py

from playwright.async_api import async_playwright, Browser, Page
from typing import Optional


class BrowserManager:
    def __init__(self):
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.page: Optional[Page] = None

    async def start_browser(self, headless: bool = True):
        self.playwright = await async_playwright().start()
        self.browser = await self.playwright.chromium.launch(headless=headless)
        self.page = await self.browser.new_page()

    async def close_browser(self):
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()

    def get_page(self) -> Page:
        if not self.page:
            raise RuntimeError("Browser has not been initialized.")
        return self.page
