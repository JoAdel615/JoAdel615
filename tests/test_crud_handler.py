from src.crud.crud_handler import CRUDHandler

def test_create():
    handler = CRUDHandler()
    result = handler.create("test_collection", {"name": "test"})
    assert result["message"] == "Document created"
