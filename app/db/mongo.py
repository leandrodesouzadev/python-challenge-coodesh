from pymongo import MongoClient
from typing import Generator
from app.core.config import settings


def get_client() -> Generator:
    try:
        client = MongoClient(settings.MONGO_URI)
        yield client
    finally:
        client.close()
