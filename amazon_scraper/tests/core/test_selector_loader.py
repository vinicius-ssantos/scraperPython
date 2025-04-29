import yaml
import pytest
from amazon_scraper.scraper_selectors.selector_loader import SelectorLoader

def test_load_selectors_success(tmp_path, monkeypatch):
    # Cria um YAML de teste
    data = {
        "foo": ["bar"],
        "search_url_template": "http://example.com?q={query}"
    }
    file = tmp_path / "selectors.yml"
    file.write_text(yaml.safe_dump(data), encoding="utf-8")

    # Faz o loader apontar para nosso arquivo temporário
    monkeypatch.setattr(
        "amazon_scraper.scraper_selectors.selector_loader.SelectorLoader.load_selectors",
        staticmethod(lambda path=str(file): data)
    )

    selectors = SelectorLoader.load_selectors(path=str(file))
    assert selectors["foo"] == ["bar"]
    assert "search_url_template" in selectors

def test_load_selectors_file_not_found():
    with pytest.raises(FileNotFoundError):
        SelectorLoader.load_selectors(path="nao_existe.yml")
