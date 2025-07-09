PREDEFINED_STRATEGIES = [

    {
        "name": "RSI Oversold",
        "conditions": [
            {
                "indicator": "rsi",
                "operator": "<",
                "value": "30"
            }
        ],
        "action": "buy"
    },

    {
        "name": "EMA Crossover",
        "conditions": [
            {
                "indicator": "ema20",
                "operator": "crosses_above",
                "value": "ema50"
            }
        ],
        "action": "buy"
    },

    {
        "name": "MACD Bullish",
        "conditions": [
            {
                "indicator": "macd",
                "operator": ">",
                "value": "0"
            }
        ],
        "action": "buy"
    },

    {
        "name": "ADX Strong Trend",
        "conditions": [
            {
                "indicator": "adx",
                "operator": ">",
                "value": "25"
            }
        ],
        "action": "buy"
    },

    {
        "name": "Bollinger Rebound",
        "conditions": [
            {
                "indicator": "close",
                "operator": "<",
                "value": "bollinger_lower"
            }
        ],
        "action": "buy"
    }

]