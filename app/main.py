from fastapi import FastAPI
from fastapi import Depends
from datetime import datetime
from datetime import timedelta
from pymongo import MongoClient
from app.routers import products
from app.db.mongo import get_client
from app.core.config import settings


app = FastAPI()
app.include_router(products.router)

@app.get("/")
def root(client: MongoClient = Depends(get_client)):
    uptime: timedelta = datetime.utcnow() - settings.SERVER_STARTED_AT
    scraper = client.food.scraper.find_one(
        {"name": "Food Scraper"},
        projection={'_id': False}
    )
    return {
        "status": "online",
        "uptime": str(uptime),
        "scraper": scraper
    }
