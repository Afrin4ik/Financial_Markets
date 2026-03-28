from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn
from .controllers.market import router as market_router


BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "views" / "static"
INDEX_HTML = BASE_DIR / "views" / "templates" / "index.html"


app = FastAPI(
    title="Financial Markets API",
    description="API для получения свечей и рисовки графиков",
)

app.include_router(router=market_router)
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
def root() -> FileResponse:
    return FileResponse(INDEX_HTML)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
