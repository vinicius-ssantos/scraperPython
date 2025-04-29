FROM python:3.11-slim

# Definir diretório de trabalho
WORKDIR /app

# Garantir que o /app esteja no PYTHONPATH para import de amazon_scraper
ENV PYTHONPATH=/app

# Instalar dependências de SO necessárias para Playwright
RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libgbm1 libxcomposite1 libxdamage1 libxrandr2 libxshmfence1 libgtk-3-0 libasound2 libpangocairo-1.0-0 libpango-1.0-0 libdbus-1-3 libexpat1 libxcb1 libx11-xcb1 libx11-6 ca-certificates fonts-liberation wget \
  && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências (inclui httpx para testes FastAPI)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Baixar navegadores para Playwright
RUN playwright install --with-deps

# Copiar todo o código do scraper
COPY . .

# Configurar entrypoint para rodar testes ou scraper
ENTRYPOINT ["bash", "-c"]
CMD ["pytest --maxfail=1 --disable-warnings -q"]