# core/fallback_selector_resolver.py
from typing import List, Optional

class FallbackSelectorResolver:
    @staticmethod
    async def resolve_text(element, selectors: List[str]) -> Optional[str]:
        for selector in selectors:
            try:
                sub_element = await element.query_selector(selector)
                if sub_element:
                    text = await sub_element.inner_text()
                    if text:
                        return text.strip()
            except Exception:
                continue
        return None

    @staticmethod
    async def resolve_attribute(element, selectors: List[str], attribute: str) -> Optional[str]:
        for selector in selectors:
            try:
                sub_element = await element.query_selector(selector)
                if sub_element:
                    attr = await sub_element.get_attribute(attribute)
                    if attr:
                        return attr.strip()
            except Exception:
                continue
        return None

