# amazon_scraper/selector_loader.py

import yaml
import os

class SelectorLoader:
    @staticmethod
    def load_selectors(path: str = "../selectors/selectors_amazon.yml") -> dict:
        full_path = os.path.join(os.path.dirname(__file__), path)
        with open(full_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
