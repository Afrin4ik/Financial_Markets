from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from .controllers.market import router as market_router
from .controllers.pages import router as pages_router
from .config.paths import STATIC_DIR

app = FastAPI(
    title="Financial Markets API",
    description="API для получения свечей и рисовки графиков",
)

app.include_router(router=market_router)
app.include_router(router=pages_router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
