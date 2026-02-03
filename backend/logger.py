from loguru import logger
import os
import sys

LOG_DIR = "logs"
LOG_FILE = f"{LOG_DIR}/app.log"

# Create directory if not exists
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

# Remove default logger
logger.remove()

# Log format (JSON recommended)
logger.add(
    sys.stdout,
    serialize=True,  # This outputs proper JSON
    level="INFO",
)

# Add file logger
logger.add(
    LOG_FILE,
    rotation="10 MB",
    retention="14 days",
    compression="zip",
    level="INFO",
    serialize=True   # <-- important for Elasticsearch / JSON logs
)

# Also log to stdout
logger.add(
    sink=lambda msg: print(msg, end=""),
    level="INFO"
)

def get_logger():
    return logger