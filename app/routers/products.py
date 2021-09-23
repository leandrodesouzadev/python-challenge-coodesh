from fastapi import APIRouter
from fastapi import Depends
from pymongo import MongoClient
from pymongo import ReturnDocument
from app.db.mongo import get_client
from app.dependencies.products import get_product_by_code_or_raise_404
from app.dependencies.pagination import pagination_parameters


router = APIRouter(prefix='/products')


@router.get('/')
def get_all_products(client: MongoClient = Depends(get_client), pagination: dict = Depends(pagination_parameters)):
    products = [p for p in client.food.info.find(projection={'_id': False}, **pagination)]
    return products


@router.get('/{code}')
def get_product_info(product: dict = Depends(get_product_by_code_or_raise_404)):
    return product


@router.put('/{code}')
def update_product(
    payload: dict,
    product: dict = Depends(get_product_by_code_or_raise_404),
    client: MongoClient = Depends(get_client)
):
    result = client.food.info.find_one_and_update(
        {'code': product['code']},
        {'$set': payload},
        projection={'_id': False},
        return_document=ReturnDocument.AFTER
    )
    return result


@router.delete('/{code}')
def delete_product(product: dict = Depends(get_product_by_code_or_raise_404), client: MongoClient = Depends(get_client)):
    
    result = client.food.info.find_one_and_update(
        {'code': product['code']},
        {'$set': {'status': 'trash'}},
        projection={'_id': False},
        return_document=ReturnDocument.AFTER
    )
    return result
