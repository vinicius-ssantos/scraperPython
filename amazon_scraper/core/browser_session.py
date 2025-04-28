# core/browser_session.py

from abc import ABC, abstractmethod

class BrowserSession(ABC):
    @abstractmethod
    async def start(self, headless: bool = True):
        """Inicializa o navegador."""
        pass

    @abstractmethod
    async def close(self):
        """Fecha o navegador."""
        pass

    @abstractmethod
    def get_page(self):
        """Retorna a página atual."""
        pass
