class SchemaVersioner:
    def __init__(self):
        self.versions = {}

    def get_version(self, collection_name):
        """Dynamically assign schema versions for collections."""
        if collection_name not in self.versions:
            self.versions[collection_name] = "v1.0.0"
        return self.versions[collection_name]

    def update_version(self, collection_name):
        """Increment version on schema changes."""
        current_version = self.versions.get(collection_name, "v1.0.0")
        major, minor, patch = map(int, current_version[1:].split("."))
        self.versions[collection_name] = f"v{major}.{minor + 1}.0"
