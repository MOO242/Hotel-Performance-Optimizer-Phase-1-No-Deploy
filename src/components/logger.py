import logging
import os
from datetime import datetime

# ---------------------------------------------------------
# 1. Create a folder for today's date
# ---------------------------------------------------------
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Folder name = today's date (YYYY_MM_DD)
TODAY = datetime.now().strftime("%Y_%m_%d")
DAILY_LOG_DIR = os.path.join(ROOT_DIR, "log", TODAY)

os.makedirs(DAILY_LOG_DIR, exist_ok=True)

# ---------------------------------------------------------
# 2. Create ONE log file for the entire day
# ---------------------------------------------------------
LOG_FILE_PATH = os.path.join(DAILY_LOG_DIR, f"{TODAY}.log")

# ---------------------------------------------------------
# 3. Define log format
# ---------------------------------------------------------
LOG_FORMAT = (
    "[ %(asctime)s ] — Line: %(lineno)d — %(name)s — %(levelname)s — %(message)s"
)

# ---------------------------------------------------------
# 4. Configure logging
# ---------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format=LOG_FORMAT,
    handlers=[
        logging.FileHandler(LOG_FILE_PATH, mode="a"),  # append mode
        logging.StreamHandler(),
    ],
)

# ---------------------------------------------------------
# 5. Export logger
# ---------------------------------------------------------

logger = logging.getLogger("hotel_pricing")
