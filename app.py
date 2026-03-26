from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Financial Markets Application",
    description="This is a simple FastAPI application",
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_items(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
