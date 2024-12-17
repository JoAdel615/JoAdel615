from pymongo import MongoClient, errors
from src.observability.logger import logger

class MongoDBHandler:
    """
    Handles MongoDB interactions.
    """

    def __init__(self, uri="mongodb://localhost:27017", db_name="json_management_db"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def insert_document(self, collection, document):
        try:
            result = self.db[collection].insert_one(document)
            logger.info(f"Document inserted in {collection} with ID {result.inserted_id}")
            return result.inserted_id
        except errors.PyMongoError as e:
            logger.error(f"Error inserting document: {e}")
            raise e

    def fetch_document(self, collection, query):
        try:
            return self.db[collection].find_one(query)
        except errors.PyMongoError as e:
            logger.error(f"Error fetching document: {e}")
            raise e
