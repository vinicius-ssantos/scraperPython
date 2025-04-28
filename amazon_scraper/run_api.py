# amazon_scraper/run_api.py

import uvicorn

if __name__ == "__main__":
    uvicorn.run("amazon_scraper.api.scraper_api:app", host="0.0.0.0", port=8001, reload=False)
