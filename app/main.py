from fastapi import FastAPI
import uvicorn
from .controllers.market import router as market_router


app = FastAPI(
    title="Financial Markets API",
    description="API для получения свечей и рисовки графиков",
)

app.include_router(router=market_router)

@app.get("/")
def root():
    return {"service": "financial-markets", "status": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
