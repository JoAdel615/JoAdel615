import unittest
from src.jsonld.jsonld_handler import JSONLDHandler

class TestJSONLDHandler(unittest.TestCase):
    def test_validate_schema(self):
        handler = JSONLDHandler()
        schema = {"@context": {}, "name": "example"}
        self.assertTrue(handler.validate_schema(schema))
