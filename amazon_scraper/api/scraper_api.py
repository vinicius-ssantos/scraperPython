# amazon_scraper/api/scraper_api.py
from fastapi import FastAPI
from amazon_scraper.api.router import router

app = FastAPI(
    title="Amazon Scraper API",
    description="API para realizar scraping de produtos na Amazon",
    version="1.0.0"
)

app.include_router(router, prefix="/api")