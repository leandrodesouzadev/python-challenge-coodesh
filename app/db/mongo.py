from pymongo import MongoClient
from typing import Generator


def get_client() -> Generator:
    try:
        client = MongoClient()
        yield client
    finally:
        client.close()
