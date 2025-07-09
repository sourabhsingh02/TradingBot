from fastapi import FastAPI
from routes.dashboard import router as data_router
from routes.strategy  import router as strategy_router
from routes.symbols import  router as symbols_router
from routes.wishlist import router as wishlist_router
from routes.nse import router as nse_router
from routes.forex import router as forex_router
from Test.Backtesting import router as backTesting_router

app = FastAPI(title="TradingBot API")


@app.get("/")
def root():
    return {"msg": "hello"}

# attach all /api routes
app.include_router(data_router)
app.include_router(strategy_router)
app.include_router(symbols_router)
app.include_router(wishlist_router)
app.include_router(nse_router)
app.include_router(forex_router)
app.include_router(backTesting_router)

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(app, host="127.0.0.1", port=8080)


