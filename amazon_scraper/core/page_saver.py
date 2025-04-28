# core/page_saver.py
import os
from datetime import datetime

class PageSaver:
    @staticmethod
    async def save_html(page, query: str, base_path: str = "output") -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(f"{base_path}/pages", exist_ok=True)
        html_content = await page.content()
        file_path = f"{base_path}/pages/page_{query}_{timestamp}.html"
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        return file_path

    @staticmethod
    async def save_screenshot(page, query: str, base_path: str = "output") -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        os.makedirs(f"{base_path}/screenshots", exist_ok=True)
        file_path = f"{base_path}/screenshots/screenshot_{query}_{timestamp}.png"
        await page.screenshot(path=file_path, full_page=True)
        return file_path

