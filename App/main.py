from fastapi import FastAPI
from routes.strategy  import router as strategy_router
from routes.symbols import  router as symbols_router
from routes.wishlist import router as wishlist_router
from routes.forex import router as forex_router
from Test.Backtesting import router as backTesting_router
from routes.data import router as data_router
from routes.dashboard import router as dashboard_router
from Test.test import router as test_router
from routes.mt5_cred import router as mt5_router
from routes.user import router as user_router
app = FastAPI(title="TradingBot API")

@app.get("/")
def root():
    return {"msg": "hello"}

# attach all /api routes
app.include_router(user_router)
app.include_router(data_router)
app.include_router(backTesting_router)
app.include_router(symbols_router)
app.include_router(wishlist_router)
app.include_router(strategy_router)
app.include_router(dashboard_router)
app.include_router(test_router)
app.include_router(mt5_router)
# app.include_router(forex_router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)


