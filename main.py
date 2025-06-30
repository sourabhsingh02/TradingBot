from fastapi import FastAPI
from routes.data import router as data_router
from routes.strategy  import router as strategy_router
from routes.symbols import  router as symbols_router
from routes.wishlist import router as wishlist_router



app = FastAPI(title="TradingBot API")

# root check
@app.get("/")
def root():
    return {"msg": "hello"}

# attach all /api routes
app.include_router(data_router)
app.include_router(strategy_router)
app.include_router(symbols_router)
app.include_router(wishlist_router)
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)

