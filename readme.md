# Advanced Auto Trading Bot - README

## How to setup - 

1. Clone the repository:
```
        git clone https://github.com/{your-repo}/auto-trading-bot.git
        cd advanced-auto-trading-bot
```


2. Install packages:
```
        pip install -r requirements.txt
```


Or manually run this :
```
        pip install fastapi uvicorn pydantic mysql-connector-python MetaTrader5 pandas

```

3. Configure database connection in *database/db_connection.py*. 
    Add predefined/custom strategies in the database if not already present.
    
#### Database Backup:

A backup of the database is available as trading_bot_db.sql. You can restore it with:
```
mysql -u root -p trading_platform < trading_bot_db.sql

```

4. Add MT5 credentials for each user in Security/encryption_mt5.py.


5. Add predefined/custom strategies in the database.



### Prerequisites

Python 3.10+

MetaTrader 5 installed and configured.

MySQL / MariaDB database.

Internet connection.


### 2️⃣ Flow of Code

1. User sends a request with ***symbols, lot, and interval.***


2. Backend fetches all ***predefined and custom strategies.***


3. For each symbol, matching strategies are applied.


4. Each (strategy, symbol) combination runs in its ***own thread.***


5. Threads fetch ***historical data***, evaluate strategy conditions, and ***place trades*** automatically.


6. Users can ***check active strategies*** or unapply them.



### 3️⃣ How to Run and Use

#### Run FastAPI server
```
uvicorn main:app --host 0.0.0.0 --port 8000 --reload

```

#### Open Swagger UI:

``` 
http://localhost:8000/docs
```

### Notes

MetaTrader 5 must be ***running and logged in.***


Console logs show ***buy/sell actions*** and scheduling information.