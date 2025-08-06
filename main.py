from fastapi import FastAPI
from routes.auto_order  import router as  auto_order_router
from routes.symbols import  router as symbols_router
from routes.wishlist import router as wishlist_router
from routes.forex import router as forex_router
from Test.Backtesting import router as backTesting_router
from routes.data import router as data_router
from routes.dashboard import router as dashboard_router
from routes.mt5_cred import router as mt5_router
from routes.user import router as user_router
from routes.order import router as order_router
from routes.history import router as history_router
from routes.custom_strategies import router as custom_strategy_router
from routes.built_in_strategies import router as built_in_strategy_router
from Admin.admin_routes.admin import  router as admin_router
from Admin.admin_routes.user import router as admin_user_router
from Admin.admin_routes.custom_strategy import router as admin_custom_strategy_router
from Admin.admin_routes.predefined_strategy import router as admin_predefined_strategy_router
from Test.Backtesing_db import router as backTesting_db_router


app = FastAPI(title="TradingBot API")

@app.get("/")
def root():
    return {"msg": "hello"}

# attach all /api routes
app.include_router(user_router)
app.include_router(mt5_router)
app.include_router(built_in_strategy_router)
app.include_router(custom_strategy_router)
app.include_router(backTesting_db_router)
app.include_router(symbols_router)
app.include_router(order_router)
app.include_router(auto_order_router)
app.include_router(history_router)
app.include_router(data_router)
app.include_router(backTesting_router)
app.include_router(wishlist_router)
app.include_router(dashboard_router)
app.include_router(admin_custom_strategy_router)
app.include_router(admin_user_router)
app.include_router(admin_predefined_strategy_router)
app.include_router(admin_router)



# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="127.0.0.1", port=8080)
#
#
