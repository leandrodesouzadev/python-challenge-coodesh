import os
import gzip
import json
import requests
import datetime
from pymongo import MongoClient
from typing import List


class FoodScraper():
    URL: str = 'https://challenges.coode.sh'
    TEMP_ZIP_FILENAME: str = 'temp.zip'
    TEMP_JSON_FILENAME: str = 'temp.json'
    MAX_ITEMS_PER_FILE: int = 100
    MAX_BYTES_TO_READ_FROM_ZIP: int = 1000000

    def __enter__(self):
        client = MongoClient()
        self.client = client
        self.db = client.food
        return self

    def __exit__(self, exc_type, exc_value, trace):
        self.client.close()
        self._cleanup_temporary_files()

    def get_files_to_read(self, ):
        list_files_response = self._make_list_files_request()
        text = list_files_response.text
        files = text.split('\n')
        return [file for file in files if len(file)]

    def _make_list_files_request(self) -> requests.Response:
        url = f'{self.URL}/food/data/json/index.txt'
        response = requests.get(url)
        assert response.status_code == 200
        return response

    def do_work(self):
        files = self.get_files_to_read()
        for filename in files:
            self.proccess_file(filename)

    def proccess_file(self, filename: str) -> None:
        started_at = datetime.datetime.utcnow()
        if self._has_already_fetched_file(filename):
            self._finish_import_in_mongo(
                filename=filename,
                started_at=started_at,
                finished_at=datetime.datetime.utcnow(),
                status='FINISHED',
                message='File was already fetched'
            )
            return
        
        self._download_zipfile(filename)
        self._unzip_contents_to_json_file()
        products = self._get_products_from_json_file()
        for product in products:
            self._insert_product_into_mongo(product)
        self._finish_import_in_mongo(
            filename=filename,
            started_at=started_at,
            finished_at=datetime.datetime.utcnow(),
            status='FINISHED',
            message='File succesfully fetched'
        )

    def _has_already_fetched_file(self, file_name) -> bool:
        collection = self.db.imports
        docs = collection.count_documents({'filename': file_name})
        return docs > 0

    def _download_zipfile(self, file_name: str) -> None:
        file_url = f'{self.URL}/food/data/json/{file_name}'
        response = requests.get(file_url)

        with open(self.TEMP_ZIP_FILENAME, 'wb') as f:
            f.write(response.content)

    def _unzip_contents_to_json_file(self) -> None:
        with open(self.TEMP_JSON_FILENAME, 'wb') as f:
            zipfile = gzip.open(self.TEMP_ZIP_FILENAME)
            f.write(zipfile.read(self.MAX_BYTES_TO_READ_FROM_ZIP))
            zipfile.close()

    def _get_products_from_json_file(self) -> List[dict]:
        with open(self.TEMP_JSON_FILENAME, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')[:self.MAX_ITEMS_PER_FILE]
            return [json.loads(line) for line in lines]
    
    def _insert_product_into_mongo(self, product: dict) -> None:
        collection = self.db.info
        product['status'] = 'draft'
        product['imported_t'] = datetime.datetime.utcnow().isoformat()
        collection.insert_one(product)

    def _finish_import_in_mongo(self, filename: str, started_at: datetime.datetime, finished_at: datetime.datetime, status: str, message: str) -> None:
        ellapsed_timedelta: datetime.timedelta = finished_at - started_at
        collection = self.db.imports
        collection.insert_one(
            {
                'filename': filename,
                'started_at': started_at.isoformat(),
                'finished_at': finished_at.isoformat(),
                'ellapsed': str(ellapsed_timedelta),
                'status': status,
                'message': message,
            }
        )

    def _cleanup_temporary_files(self):
        files_to_remove = [self.TEMP_ZIP_FILENAME, self.TEMP_JSON_FILENAME]
        for file in files_to_remove:
            try:
                os.remove(file)
            except FileNotFoundError:
                print(f"Couldn't remove temporary file: {file} proceeding..")
