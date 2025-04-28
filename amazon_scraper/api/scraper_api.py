# api/scraper_api.py

from fastapi import FastAPI, Query, HTTPException
from ..scraper import AmazonScraper
from ..model import Product
from typing import List
from loguru import logger

app = FastAPI(title="Amazon Scraper API", version="1.0.0")

scraper = AmazonScraper()

@app.on_event("startup")
async def startup_event():
    logger.info("Starting browser instance...")
    await scraper.init_browser()

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Closing browser instance...")
    await scraper.close()

@app.get("/scrape", response_model=List[Product])
async def scrape_products(query: str = Query(..., description="Search keyword for Amazon scraping")):
    try:
        products = await scraper.scrape(query)
        return products
    except Exception as e:
        logger.error(f"Scraping failed: {e}")
        raise HTTPException(status_code=500, detail="Scraping failed. Check logs for more details.")
