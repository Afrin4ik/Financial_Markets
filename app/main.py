import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from .controllers.market import router as market_router
from .controllers.pages import router as pages_router
from .config.paths import STATIC_DIR

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# отключение шумных INFO-логов внутреннего клиента Tinkoff (GetCandles на каждую страницу данных)
logging.getLogger("tinkoff.invest").setLevel(logging.WARNING)
logging.getLogger("tinkoff.invest.logging").setLevel(logging.WARNING)

logger.info("Инициализация Financial Markets API")

app = FastAPI(
    title="Financial Markets API",
    description="API для получения свечей и рисовки графиков",
)

logger.info("Подключение роутеров контроллеров")
app.include_router(router=market_router)
app.include_router(router=pages_router)

if STATIC_DIR.exists():
    logger.info(f"Монтирование статических файлов из {STATIC_DIR}")
    app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
else:
    logger.critical(f"Папка со статикой не найдена: {STATIC_DIR}")
    raise RuntimeError(f"Папка со статикой не найдена: {STATIC_DIR}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
