from jsonschema import validate, ValidationError

class SchemaValidator:
    @staticmethod
    def validate_data(data, schema):
        try:
            validate(instance=data, schema=schema)
            return True
        except ValidationError as e:
            return False, e.message
