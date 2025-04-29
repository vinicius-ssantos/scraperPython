#!/usr/bin/env bash
set -euo pipefail

# Builda a imagem
docker build -t amazon-scraper:test .

# Executa testes dentro do container
docker run --rm -v "$(pwd)/output":/app/output -v "$(pwd)/logs":/app/logs amazon-scraper:test \
    pytest --maxfail=1 --disable-warnings -q
