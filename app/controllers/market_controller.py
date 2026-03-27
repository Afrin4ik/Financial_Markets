from fastapi import FastAPI


app = FastAPI(
    title="My FastAPI Application",
    description="This is a sample FastAPI application.",
)

@app.get("/chart")
def read_chart(figi: str, days: int, timeframe: str):
    # Здесь будет логика для получения данных и построения графика
    return {"message": f"Получение данных для FIGI: {figi}, за последние {days} дней, с таймфреймом {timeframe}"}
