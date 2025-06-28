from fastapi import FastAPI
from routes.data import router as data_router

app = FastAPI(title="TradingBot Dummy API")

# root check
@app.get("/")
def root():
    return {"msg": "hello"}

# attach all /api routes
app.include_router(data_router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)

