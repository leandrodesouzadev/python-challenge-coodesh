import time
import datetime
from schedule import repeat
from schedule import every
from schedule import run_pending
from schedule import run_all
from app.scraper.food_scraper import FoodScraper
from pymongo import MongoClient


@repeat(every().day.at("00:00"))
def start_scraper():
    with FoodScraper() as scraper:
        scraper.do_work()
    client, collection = get_mongo_client_collection()
    send_worker_has_ran_to_mongo(collection)
    client.close()

def get_mongo_client_collection():
    client = MongoClient()
    collection = client.food.scraper
    return client, collection

def send_worker_is_online_to_mongo(collection):
    documents_count = collection.count_documents({})
    if documents_count == 0:
        create_worker_document(collection)
    collection.find_one_and_update(
        {'name': 'Food Scraper'},
        {'$set': {
            'status': 'online',
            'last_online_at': datetime.datetime.utcnow().isoformat(),
        }}
    )

def send_worker_has_ran_to_mongo(collection):
    collection.find_one_and_update(
        {},
        {
            '$inc': {
                'times_ran': 1
            },
            '$set': {
                'last_finished_job_at': datetime.datetime.utcnow().isoformat()
            }
        }
    )

def create_worker_document(collection):
    now = datetime.datetime.utcnow().isoformat()
    collection.insert_one({
        'name': 'Food Scraper',
        'first_started_at': now,
        'last_online_at': now,
        'last_finished_job_at': None,
        'online': True,
        'offline_since': None,
        'times_ran': 0
    })

if __name__ == "__main__":
    first_time = True
    while True:
        client, collection = get_mongo_client_collection()
        send_worker_is_online_to_mongo(collection)
        client.close()
        if first_time:
            run_all()
            first_time = False
        else:
            run_pending()
        time.sleep(60)
