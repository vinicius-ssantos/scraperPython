# amazon_scraper/model.py

from pydantic import BaseModel

class Product(BaseModel):
    title: str
    price: str | None = None
    rating: str | None = None
    reviews: str | None = None
    link: str | None = None
    image_url: str | None = None
    delivery: str | None = None
    badge: str | None = None
    asin: str | None = None
