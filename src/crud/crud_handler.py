from pymongo import MongoClient
from fastapi import HTTPException
from jsonschema import validate, ValidationError
import logging
import time

from src.crud.audit_logger import AuditLogger
from src.database.schema_versioner import SchemaVersioner

class CRUDHandler:
    def __init__(self, db_uri="mongodb://127.0.0.1:27017", database_name="json_management"):
        self.client = MongoClient(db_uri)
        self.db = self.client[database_name]
        self.logger = AuditLogger()
        self.versioner = SchemaVersioner()

    def create(self, collection_name: str, document: dict, schema: dict = None):
        """Insert a document with optional schema validation."""
        collection = self.db[collection_name]
        try:
            # Intelligent schema validation
            if schema:
                validate(instance=document, schema=schema)
            else:
                logging.warning("No schema provided for validation. Proceeding with insertion.")

            # Add schema versioning and timestamps
            document["_created_at"] = time.time()
            document["_schema_version"] = self.versioner.get_version(collection_name)

            result = collection.insert_one(document)
            self.logger.log_event("CREATE", collection_name, document)

            return {"message": "Document created successfully", "id": str(result.inserted_id)}

        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Schema validation failed: {e.message}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def read(self, collection_name: str, query: dict = None):
        """Fetch documents based on query."""
        collection = self.db[collection_name]
        try:
            documents = list(collection.find(query or {}))
            self.logger.log_event("READ", collection_name, {"query": query})
            return documents
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def update(self, collection_name: str, query: dict, update_data: dict, schema: dict = None):
        """Update documents with optional schema validation."""
        collection = self.db[collection_name]
        try:
            if schema:
                validate(instance=update_data, schema=schema)

            result = collection.update_many(query, {"$set": update_data})
            self.logger.log_event("UPDATE", collection_name, {"query": query, "updates": update_data})

            return {"message": "Documents updated", "modified_count": result.modified_count}
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Schema validation failed: {e.message}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    def delete(self, collection_name: str, query: dict):
        """Delete documents based on query."""
        collection = self.db[collection_name]
        try:
            result = collection.delete_many(query)
            self.logger.log_event("DELETE", collection_name, {"query": query})

            return {"message": "Documents deleted", "deleted_count": result.deleted_count}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
