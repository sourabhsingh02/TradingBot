# predefined_strategies.py

PREDEFINED_STRATEGIES = [
    {
        "name": "RSI Oversold",
        "conditions": [
            { "indicator": "RSI_14", "operator": "<", "value": "30" }
        ],
        "action": "BUY"
    },
    {
        "name": "RSI Overbought",
        "conditions": [
            { "indicator": "RSI_14", "operator": ">", "value": "70" }
        ],
        "action": "SELL"
    },
    {
        "name": "Golden Crossover",
        "conditions": [
            { "indicator": "SMA_20", "operator": ">", "value": "SMA_50" }
        ],
        "action": "BUY"
    },
    {
        "name": "MACD Bullish",
        "conditions": [
            { "indicator": "MACD", "operator": ">", "value": "MACD_signal" }
        ],
        "action": "BUY"
    },
    {
        "name": "Strong Uptrend",
        "conditions": [
            { "indicator": "Close", "operator": ">", "value": "SMA_200" }
        ],
        "action": "BUY"
    }
]

