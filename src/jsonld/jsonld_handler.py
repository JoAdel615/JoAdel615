from pyld import jsonld

class JSONLDHandler:
    def __init__(self):
        pass

    def create_schema(self, schema: dict):
        return jsonld.compact(schema, {"@context": schema.get("@context", {})})
