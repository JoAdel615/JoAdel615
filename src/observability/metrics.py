from observability.logger import logger
from prometheus_client import Counter, start_http_server

SCHEMA_VALIDATIONS = Counter('schema_validations', 'Number of validated schemas')
SCHEMA_UPDATES = Counter('schema_updates', 'Number of schema updates performed')

def start_metrics_server(port=8001):
    start_http_server(port)
    logger.info(f"Metrics server started on port {port}")
