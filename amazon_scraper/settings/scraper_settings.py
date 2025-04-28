# settings/scraper_settings.py
class ScraperSettings:
    OUTPUT_BASE_PATH = "output"
    SCREENSHOTS_PATH = f"{OUTPUT_BASE_PATH}/screenshots"
    HTML_PAGES_PATH = f"{OUTPUT_BASE_PATH}/pages"
    PRODUCTS_JSON_PATH = f"{OUTPUT_BASE_PATH}/products"
    SELECTOR_FILE_PATH = "scraper_selectors/selectors_amazon.yml"

