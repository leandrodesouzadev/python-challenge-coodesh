from pydantic import BaseSettings
from datetime import datetime


class Settings(BaseSettings):

    PROJECT_NAME: str = 'Food Products API'
    MAX_ITEMS_PER_PAGE: int = 100
    DEFAULT_ITEMS_PER_PAGE: int = 50
    SERVER_STARTED_AT: datetime = datetime.utcnow()
    

settings = Settings()
