import logging

class AuditLogger:
    def __init__(self):
        logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
        self.logger = logging.getLogger("AuditLogger")

    def log_event(self, event_type: str, collection: str, data: dict):
        self.logger.info(f"{event_type} on collection {collection}: {data}")
