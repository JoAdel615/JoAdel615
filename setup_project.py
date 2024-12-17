import os

# Project Directories and Files
PROJECT_STRUCTURE = {
    "src": {
        "api": {
            "main.py": '''import os
from fastapi import FastAPI
from src.crud.crud_handler import CRUDHandler
from src.external.external_api_handler import ExternalAPIHandler

app = FastAPI(
    title="Enhanced JSON-LD Service",
    version="2.0.0",
    description="A service for managing, validating, and dynamically integrating JSON-LD schemas."
)

crud_handler = CRUDHandler()
external_api = ExternalAPIHandler()

@app.get("/")
def root():
    return {"message": "Welcome to the Enhanced JSON-LD Management Service"}

@app.post("/create/{collection}")
def create_document(collection: str, document: dict):
    return crud_handler.create(collection, document)

@app.get("/read/{collection}")
def read_documents(collection: str, query: dict = None):
    return crud_handler.read(collection, query)

@app.put("/update/{collection}")
def update_document(collection: str, query: dict, updates: dict):
    return crud_handler.update(collection, query, updates)

@app.delete("/delete/{collection}")
def delete_document(collection: str, query: dict):
    return crud_handler.delete(collection, query)

@app.get("/fetch-external/")
def fetch_external_data(url: str, params: dict = None):
    return external_api.fetch_data(url, params)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 8000)), reload=True)
''',
        },
        "crud": {
            "crud_handler.py": '''from pymongo import MongoClient
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
        collection = self.db[collection_name]
        try:
            if schema:
                validate(instance=document, schema=schema)
            document["_created_at"] = time.time()
            document["_schema_version"] = self.versioner.get_version(collection_name)
            result = collection.insert_one(document)
            self.logger.log_event("CREATE", collection_name, document)
            return {"message": "Document created", "id": str(result.inserted_id)}
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Schema validation failed: {e.message}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
''',
            "audit_logger.py": '''import logging

class AuditLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger("AuditLogger")

    def log_event(self, event_type: str, collection: str, data: dict):
        self.logger.info(f"{event_type} on collection {collection}: {data}")
''',
        },
        "external": {
            "external_api_handler.py": '''import requests

class ExternalAPIHandler:
    def fetch_data(self, url: str, params: dict = None):
        response = requests.get(url, params=params)
        if response.status_code != 200:
            raise Exception(f"API request failed: {response.status_code}")
        return response.json()
''',
        },
        "database": {
            "schema_versioner.py": '''class SchemaVersioner:
    def __init__(self):
        self.versions = {}

    def get_version(self, collection_name):
        if collection_name not in self.versions:
            self.versions[collection_name] = "v1.0.0"
        return self.versions[collection_name]
''',
        },
        "utils": {
            "observability.py": '''import logging

def configure_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    return logging.getLogger("ObservabilityLogger")
''',
            "error_handler.py": '''from fastapi.responses import JSONResponse
from fastapi.requests import Request

async def custom_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"message": "An internal server error occurred", "detail": str(exc)},
    )
''',
        },
    },
    "tests": {
        "test_crud_handler.py": '''from src.crud.crud_handler import CRUDHandler

def test_create():
    handler = CRUDHandler()
    result = handler.create("test_collection", {"name": "test"})
    assert result["message"] == "Document created"
''',
    },
    "requirements.txt": '''fastapi
pymongo
requests
jsonschema
uvicorn
''',
    "README.md": "# Enhanced JSON-LD Management Service\n\nA FastAPI-powered service for managing and dynamically expanding JSON-LD schemas.",
}

# Function to create directories and files dynamically
def create_project_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_project_structure(path, content)
        else:
            with open(path, "w") as file:
                file.write(content)
            print(f"Created: {path}")

# Main script execution
if __name__ == "__main__":
    BASE_DIR = os.getcwd()
    print("Creating project structure...")
    create_project_structure(BASE_DIR, PROJECT_STRUCTURE)
    print("Project structure successfully created!")
    print("To get started, run:")
    print("\n1. Install dependencies:")
    print("   pip install -r requirements.txt")
    print("\n2. Start the service:")
    print("   uvicorn src.api.main:app --reload")
    print("\n3. Test endpoints at:")
    print("   http://127.0.0.1:8000")
