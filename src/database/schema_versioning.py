class SemanticVersioning:
    """
    Tracks and updates schema versions.
    """

    def __init__(self):
        self.version = {"major": 1, "minor": 0, "patch": 0}

    def increment(self, change_type="patch"):
        if change_type == "patch":
            self.version["patch"] += 1
        elif change_type == "minor":
            self.version["minor"] += 1
            self.version["patch"] = 0
        elif change_type == "major":
            self.version["major"] += 1
            self.version["minor"] = 0
            self.version["patch"] = 0

    def get_version(self):
        return f'v{self.version["major"]}.{self.version["minor"]}.{self.version["patch"]}'
