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


# predefined_strategies = [
#     {
#         "name": "RSI Oversold Buy",
#         "conditions": [
#             {"indicator": "rsi", "operator": "<", "value": "30"}
#         ]
#     } ,
#     {
#         "name": "RSI Overbought Sell",
#         "conditions": [
#             {"indicator": "rsi", "operator": ">", "value": "70"}
#         ]
#     },
#     {
        # "name": "MACD Bullish Crossover" , "conditions": [ {"indicator": "macd", "operator": "crosses_above", "value": "signal"} ] }, { "name": "MACD Bearish Crossover", "conditions": [ {"indicator": "macd", "operator": "crosses_below", "value": "signal"} ] }, { "name": "EMA20 Above EMA50", "conditions": [ {"indicator": "ema20", "operator": ">", "value": "ema50"} ] }, { "name": "EMA20 Below EMA50", "conditions": [ {"indicator": "ema20", "operator": "<", "value": "ema50"} ] }, { "name": "Bollinger Band Lower Bounce", "conditions": [ {"indicator": "close", "operator": "<", "value": "bb_lower"} ] }, { "name": "Bollinger Band Upper Rejection", "conditions": [ {"indicator": "close", "operator": ">", "value": "bb_upper"} ] }, { "name": "ADX Trend with EMA", "conditions": [ {"indicator": "adx", "operator": ">", "value": "25"}, {"indicator": "ema20", "operator": ">", "value": "ema50"} ] }, { "name": "SuperTrend Buy Signal", "conditions": [ {"indicator": "supertrend", "operator": "==", "value": "buy"} ] }, { "name": "SuperTrend Sell Signal", "conditions": [ {"indicator": "supertrend", "operator": "==", "value": "sell"} ] }, { "name": "Stochastic Oversold", "conditions": [ {"indicator": "stoch_k", "operator": "<", "value": "20"}, {"indicator": "stoch_d", "operator": "<", "value": "20"} ] }, { "name": "VWAP Pullback Buy", "conditions": [ {"indicator": "close", "operator": ">", "value": "vwap"}, {"indicator": "low", "operator": "<", "value": "vwap"} ] }, { "name": "Ichimoku Cloud Breakout", "conditions": [ {"indicator": "close", "operator": ">", "value": "cloud_top"} ] }, { "name": "Heikin Ashi Bullish Reversal", "conditions": [ {"indicator": "heikin_ashi", "operator": "==", "value": "bullish_reversal"} ] }, { "name": "RSI Bullish Divergence", "conditions": [ {"indicator": "rsi_divergence", "operator": "==", "value": "bullish"} ] }, { "name": "Volume Spike Buy", "conditions": [ {"indicator": "volume", "operator": ">", "value": "volume_ma"} ] }, { "name": "Donchian Channel Breakout", "conditions": [ {"indicator": "close", "operator": ">", "value": "donchian_upper"} ] }, { "name": "Fibonacci 61.8% Pullback", "conditions": [ {"indicator": "close", "operator": "approx_eq", "value": "fib_618"} ] }, { "name": "Parabolic SAR Buy", "conditions": [ {"indicator": "sar", "operator": "<", "value": "close"} ] } ]