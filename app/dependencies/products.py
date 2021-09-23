from fastapi import HTTPException
from fastapi import status
from fastapi import Depends
from pymongo import MongoClient
from app.db.mongo import get_client



def get_product_by_code_or_raise_404(code: str, client: MongoClient = Depends(get_client)) -> dict:
    product = client.food.info.find_one({'code': code}, projection={'_id': False})
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No such product"
        )
    return product
