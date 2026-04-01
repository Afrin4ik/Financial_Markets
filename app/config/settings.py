import os
import logging
from dotenv import load_dotenv


load_dotenv()
TOKEN: str | None = os.getenv("API_TOKEN")

logger = logging.getLogger(__name__)
if not TOKEN:
    logger.warning("API_TOKEN не найден в переменных окружения")
