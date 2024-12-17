import os
from fastapi import FastAPI
from src.crud.crud_handler import CRUDHandler
from src.external.external_api_handler import ExternalAPIHandler

# Initialize FastAPI app
app = FastAPI(
    title="Enhanced JSON-LD Service",
    version="2.0.0",
    description="A service for managing, validating, and dynamically integrating JSON-LD schemas."
)

# Initialize handlers
crud_handler = CRUDHandler()
external_api = ExternalAPIHandler()

# Root Endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Enhanced JSON-LD Management Service"}

# CRUD Endpoints
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

# External API Endpoint
@app.get("/fetch-external/")
def fetch_external_data(url: str, params: dict = None):
    return external_api.fetch_data(url, params)

# Run the app dynamically
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("API_PORT", 8000)), reload=True)
