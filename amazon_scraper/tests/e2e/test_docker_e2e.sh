#!/usr/bin/env bash
set -euo pipefail

# Caminho para a raiz do projeto (dois níveis acima deste script)
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"

# Build da imagem usando o Dockerfile da raiz
docker build -t amazon-scraper:test "$PROJECT_ROOT"

# Executa pytest dentro do container, montando output e logs
docker run --rm \
    -v "$PROJECT_ROOT/output":/app/output \
    -v "$PROJECT_ROOT/logs":/app/logs \
    amazon-scraper:test \
    pytest --maxfail=1 --disable-warnings -q
