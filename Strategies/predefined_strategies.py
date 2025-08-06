PREDEFINED_STRATEGIES = [

    {
        "name": "Always Match Strategy",
        "conditions": [
            {
                "indicator": "close",
                "operator": ">",
                "value": "0",   # Always true
                "action": "buy"
            },
            {
                "indicator": "close",
                "operator": "<",
                "value": "999999",  # Always true
                "action": "sell"
            }
        ]
    },

    {
      "name": "SMA Close Crossover",
      "conditions": [
        {
          "indicator": "close",
          "operator": ">",
          "value": "sma_10",
          "action": "buy"
        },
        {
          "indicator": "close",
          "operator": "<",
          "value": "sma_10",
          "action": "sell"
        }
      ]
    },
    {
        "name": "RSI Overbought/Oversold Strategy",
        "conditions": [
            {
                "indicator": "rsi",
                "operator": "<",
                "value": "30",
                "action": "buy"
            },
            {
                "indicator": "rsi",
                "operator": ">",
                "value": "70",
                "action": "sell"
            }
        ]
    },

    {
        "name": "EMA 20/50 Crossover",
        "conditions": [
            {
                "indicator": "ema20",
                "operator": "crosses_above",
                "value": "ema50",
                "action": "buy"
            },
            {
                "indicator": "ema20",
                "operator": "crosses_below",
                "value": "ema50",
                "action": "sell"
            }
        ]
    },

    {
        "name": "MACD Signal Line Cross",
        "conditions": [
            {
                "indicator": "macd_line",
                "operator": "crosses_above",
                "value": "signal_line",
                "action": "buy"
            },
            {
                "indicator": "macd_line",
                "operator": "crosses_below",
                "value": "signal_line",
                "action": "sell"
            }
        ]
    },

    {
        "name": "Bollinger Band Reversal",
        "conditions": [
            {
                "indicator": "close",
                "operator": "<",
                "value": "bollinger_lower",
                "action": "buy"
            },
            {
                "indicator": "close",
                "operator": ">",
                "value": "bollinger_upper",
                "action": "sell"
            }
        ]
    },

    {
        "name": "ADX Trend Strength",
        "conditions": [
            {
                "indicator": "adx",
                "operator": ">",
                "value": "25",
                "action": "buy"
            },
            {
                "indicator": "adx",
                "operator": "<",
                "value": "20",
                "action": "sell"
            }
        ]
    }
]
# free  20 +107
# PREDEFINED_STRATEGIES = [
#     {
#         "name": "MACD Strategy",
#         "conditions": [
#             {"indicator": "MACD", "operator": "crossover", "value": "Signal", "action": "buy"},
#             {"indicator": "MACD", "operator": "crossunder", "value": "Signal", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Moving Average Cross",
#         "conditions": [
#             {"indicator": "SMA(9)", "operator": "crossover", "value": "SMA(21)", "action": "buy"},
#             {"indicator": "SMA(9)", "operator": "crossunder", "value": "SMA(21)", "action": "sell"}
#         ]
#     },
#     {
#         "name": "RSI Strategy",
#         "conditions": [
#             {"indicator": "RSI(14)", "operator": "<", "value": 30, "action": "buy"},
#             {"indicator": "RSI(14)", "operator": ">", "value": 70, "action": "sell"}
#         ]
#     },
#     {
#         "name": "Bollinger Bands Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": "<", "value": "Lower Band", "action": "buy"},
#             {"indicator": "Close", "operator": ">", "value": "Upper Band", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Channel Breakout Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": ">", "value": "Previous High", "action": "buy"},
#             {"indicator": "Close", "operator": "<", "value": "Previous Low", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Keltner Channel Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": "<", "value": "Lower Keltner", "action": "buy"},
#             {"indicator": "Close", "operator": ">", "value": "Upper Keltner", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Moving Average Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": ">", "value": "SMA(50)", "action": "buy"},
#             {"indicator": "Close", "operator": "<", "value": "SMA(50)", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Parabolic SAR Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": ">", "value": "SAR", "action": "buy"},
#             {"indicator": "Close", "operator": "<", "value": "SAR", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Pivots High/Low Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": ">", "value": "Pivot High", "action": "buy"},
#             {"indicator": "Close", "operator": "<", "value": "Pivot Low", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Price Oscillator Strategy",
#         "conditions": [
#             {"indicator": "Price Oscillator", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "Price Oscillator", "operator": "<", "value": 0, "action": "sell"}
#         ]
#     },
#     {
#         "name": "Triple EMA Strategy",
#         "conditions": [
#             {"indicator": "EMA(9)", "operator": ">", "value": "EMA(21)", "action": "buy"},
#             {"indicator": "EMA(9)", "operator": "<", "value": "EMA(21)", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Donchian Channel Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": ">", "value": "Donchian High", "action": "buy"},
#             {"indicator": "Close", "operator": "<", "value": "Donchian Low", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Aroon Strategy",
#         "conditions": [
#             {"indicator": "Aroon Up", "operator": ">", "value": 70, "action": "buy"},
#             {"indicator": "Aroon Down", "operator": ">", "value": 70, "action": "sell"}
#         ]
#     },
#     {
#         "name": "EMA Crossover Strategy",
#         "conditions": [
#             {"indicator": "EMA(12)", "operator": "crossover", "value": "EMA(26)", "action": "buy"},
#             {"indicator": "EMA(12)", "operator": "crossunder", "value": "EMA(26)", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Supertrend Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": ">", "value": "Supertrend", "action": "buy"},
#             {"indicator": "Close", "operator": "<", "value": "Supertrend", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Ichimoku Cloud Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": ">", "value": "Cloud", "action": "buy"},
#             {"indicator": "Close", "operator": "<", "value": "Cloud", "action": "sell"}
#         ]
#     },
#     {
#         "name": "DMI Strategy",
#         "conditions": [
#             {"indicator": "DI+", "operator": ">", "value": "DI-", "action": "buy"},
#             {"indicator": "DI-", "operator": ">", "value": "DI+", "action": "sell"}
#         ]
#     },
#     {
#         "name": "VWAP Reversion Strategy",
#         "conditions": [
#             {"indicator": "Close", "operator": "<", "value": "VWAP", "action": "buy"},
#             {"indicator": "Close", "operator": ">", "value": "VWAP", "action": "sell"}
#         ]
#     },
#     {
#         "name": "MA RSI Strategy",
#         "conditions": [
#             {"indicator": "RSI(14)", "operator": "<", "value": 30, "action": "buy"},
#             {"indicator": "RSI(14)", "operator": ">", "value": 70, "action": "sell"}
#         ]
#     },
#     {
#         "name": "SSL Channel Strategy",
#         "conditions": [
#             {"indicator": "SSL Up", "operator": "crossover", "value": "SSL Down", "action": "buy"},
#             {"indicator": "SSL Up", "operator": "crossunder", "value": "SSL Down", "action": "sell"}
#         ]
#     },
#     {
#         "name": "52 Week High/Low",
#         "conditions": [
#             {"indicator": "price", "operator": "crosses_above", "value": "52_week_high", "action": "buy"},
#             {"indicator": "price", "operator": "crosses_below", "value": "52_week_low", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Accelerator Oscillator",
#         "conditions": [
#             {"indicator": "ac", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "ac", "operator": "<", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Accumulation/Distribution",
#         "conditions": [
#             {"indicator": "ad", "operator": "increasing", "value": "", "action": "buy"},
#             {"indicator": "ad", "operator": "decreasing", "value": "", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Accumulative Swing Index",
#         "conditions": [
#             {"indicator": "asi", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "asi", "operator": "<", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Advance/Decline",
#         "conditions": [
#             {"indicator": "adv_dec", "operator": ">", "value": "threshold", "action": "buy"},
#             {"indicator": "adv_dec", "operator": "<", "value": "threshold", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Arnaud Legoux Moving Average",
#         "conditions": [
#             {"indicator": "alma", "operator": "crosses_above", "value": "price", "action": "buy"},
#             {"indicator": "alma", "operator": "crosses_below", "value": "price", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Aroon",
#         "conditions": [
#             {"indicator": "aroon_up", "operator": ">", "value": 70, "action": "buy"},
#             {"indicator": "aroon_down", "operator": ">", "value": 70, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Average Directional Index",
#         "conditions": [
#             {"indicator": "adx", "operator": ">", "value": 25, "action": "buy"},
#             {"indicator": "adx", "operator": "<", "value": 20, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Average Price",
#         "conditions": [
#             {"indicator": "price", "operator": ">", "value": "average_price", "action": "buy"},
#             {"indicator": "price", "operator": "<", "value": "average_price", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Average True Range",
#         "conditions": [
#             {"indicator": "atr", "operator": "rising", "value": "", "action": "buy"},
#             {"indicator": "atr", "operator": "falling", "value": "", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Awesome Oscillator",
#         "conditions": [
#             {"indicator": "ao", "operator": "crosses_above", "value": 0, "action": "buy"},
#             {"indicator": "ao", "operator": "crosses_below", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Balance of Power",
#         "conditions": [
#             {"indicator": "bop", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "bop", "operator": "<", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Bollinger Bands",
#         "conditions": [
#             {"indicator": "price", "operator": "crosses_below", "value": "lower_band", "action": "buy"},
#             {"indicator": "price", "operator": "crosses_above", "value": "upper_band", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Bollinger Bands %B",
#         "conditions": [
#             {"indicator": "bb_percent", "operator": "<", "value": 0, "action": "buy"},
#             {"indicator": "bb_percent", "operator": ">", "value": 1, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Bollinger Bands Width",
#         "conditions": [
#             {"indicator": "bb_width", "operator": "increasing", "value": "", "action": "buy"},
#             {"indicator": "bb_width", "operator": "decreasing", "value": "", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Chaikin Money Flow",
#         "conditions": [
#             {"indicator": "cmf", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "cmf", "operator": "<", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Chaikin Oscillator",
#         "conditions": [
#             {"indicator": "cho", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "cho", "operator": "<", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Chaikin Volatility",
#         "conditions": [
#             {"indicator": "chaikin_vol", "operator": ">", "value": "threshold", "action": "buy"},
#             {"indicator": "chaikin_vol", "operator": "<", "value": "threshold", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Chande Kroll Stop",
#         "conditions": [
#             {"indicator": "price", "operator": "crosses_above", "value": "ck_stop", "action": "buy"},
#             {"indicator": "price", "operator": "crosses_below", "value": "ck_stop", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Chande Momentum Oscillator",
#         "conditions": [
#             {"indicator": "cmo", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "cmo", "operator": "<", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Double EMA",
#         "conditions": [
#             {"indicator": "DEMA", "operator": ">", "value": "price", "action": "buy"},
#             {"indicator": "DEMA", "operator": "<", "value": "price", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Ease of Movement",
#         "conditions": [
#             {"indicator": "EOM", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "EOM", "operator": "<", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Elder's Force Index",
#         "conditions": [
#             {"indicator": "EFI", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "EFI", "operator": "<", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "EMA Cross",
#         "conditions": [
#             {"indicator": "EMA_9", "operator": "crosses_above", "value": "EMA_21", "action": "buy"},
#             {"indicator": "EMA_9", "operator": "crosses_below", "value": "EMA_21", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Envelopes",
#         "conditions": [
#             {"indicator": "price", "operator": "<", "value": "LowerEnvelope", "action": "buy"},
#             {"indicator": "price", "operator": ">", "value": "UpperEnvelope", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Fisher Transform",
#         "conditions": [
#             {"indicator": "Fisher", "operator": "crosses_above", "value": 0, "action": "buy"},
#             {"indicator": "Fisher", "operator": "crosses_below", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Guppy Multiple Moving Average",
#         "conditions": [
#             {"indicator": "ShortGuppy", "operator": ">", "value": "LongGuppy", "action": "buy"},
#             {"indicator": "ShortGuppy", "operator": "<", "value": "LongGuppy", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Historical Volatility",
#         "conditions": [
#             {"indicator": "HistoricalVolatility", "operator": ">", "value": 1.5, "action": "buy"},
#             {"indicator": "HistoricalVolatility", "operator": "<", "value": 1.0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "Hull Moving Average",
#         "conditions": [
#             {"indicator": "HMA", "operator": ">", "value": "price", "action": "buy"},
#             {"indicator": "HMA", "operator": "<", "value": "price", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Ichimoku Cloud",
#         "conditions": [
#             {"indicator": "price", "operator": ">", "value": "CloudTop", "action": "buy"},
#             {"indicator": "price", "operator": "<", "value": "CloudBottom", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Keltner Channels",
#         "conditions": [
#             {"indicator": "price", "operator": "<", "value": "LowerKC", "action": "buy"},
#             {"indicator": "price", "operator": ">", "value": "UpperKC", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Klinger Oscillator",
#         "conditions": [
#             {"indicator": "Klinger", "operator": "crosses_above", "value": "Signal", "action": "buy"},
#             {"indicator": "Klinger", "operator": "crosses_below", "value": "Signal", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Know Sure Thing",
#         "conditions": [
#             {"indicator": "KST", "operator": ">", "value": "Signal", "action": "buy"},
#             {"indicator": "KST", "operator": "<", "value": "Signal", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Least Squares Moving Average",
#         "conditions": [
#             {"indicator": "LSMA", "operator": "crosses_above", "value": "price", "action": "buy"},
#             {"indicator": "LSMA", "operator": "crosses_below", "value": "price", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Linear Regression Curve",
#         "conditions": [
#             {"indicator": "price", "operator": ">", "value": "LinRegCurve", "action": "buy"},
#             {"indicator": "price", "operator": "<", "value": "LinRegCurve", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Linear Regression Slope",
#         "conditions": [
#             {"indicator": "LinRegSlope", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "LinRegSlope", "operator": "<", "value": 0, "action": "sell"},
#         ]
#     },
#     {
#         "name": "MA Cross",
#         "conditions": [
#             {"indicator": "MA_10", "operator": "crosses_above", "value": "MA_20", "action": "buy"},
#             {"indicator": "MA_10", "operator": "crosses_below", "value": "MA_20", "action": "sell"},
#         ]
#     },
#     {
#         "name": "MA with EMA Cross",
#         "conditions": [
#             {"indicator": "MA", "operator": "crosses_above", "value": "EMA", "action": "buy"},
#             {"indicator": "MA", "operator": "crosses_below", "value": "EMA", "action": "sell"},
#         ]
#     },
#     {
#         "name": "Mass Index",
#         "conditions": [
#             {"indicator": "MassIndex", "operator": "crosses_above", "value": 27, "action": "buy"},
#             {"indicator": "MassIndex", "operator": "crosses_below", "value": 26.5, "action": "sell"},
#         ]
#     },
#     {
#         "name": "McGinley Dynamic",
#         "conditions": [
#             {"indicator": "price", "operator": "crosses_above", "value": "McGinley", "action": "buy"},
#             {"indicator": "price", "operator": "crosses_below", "value": "McGinley", "action": "sell"},
#         ]
#     },
#
#     {
#         "name": "Momentum Oscillator",
#         "conditions": [
#             {"indicator": "momentum", "operator": ">", "value": 100, "action": "buy"},
#             {"indicator": "momentum", "operator": "<", "value": 100, "action": "sell"},
#         ],
#     },
#     {
#         "name": "Money Flow Index",
#         "conditions": [
#             {"indicator": "mfi", "operator": "<", "value": 20, "action": "buy"},
#             {"indicator": "mfi", "operator": ">", "value": 80, "action": "sell"},
#         ],
#     },
#     {
#         "name": "Moving Average",
#         "conditions": [
#             {"indicator": "close", "operator": ">", "value": "sma_50", "action": "buy"},
#             {"indicator": "close", "operator": "<", "value": "sma_50", "action": "sell"},
#         ],
#     },
#     {
#         "name": "Moving Average Exponential",
#         "conditions": [
#             {"indicator": "close", "operator": ">", "value": "ema_50", "action": "buy"},
#             {"indicator": "close", "operator": "<", "value": "ema_50", "action": "sell"},
#         ],
#     },
#     {
#         "name": "Moving Average Weighted",
#         "conditions": [
#             {"indicator": "close", "operator": ">", "value": "wma_50", "action": "buy"},
#             {"indicator": "close", "operator": "<", "value": "wma_50", "action": "sell"},
#         ],
#     },
#     {
#         "name": "Moving Average Ribbon",
#         "conditions": [
#             {"indicator": "sma_10", "operator": ">", "value": "sma_50", "action": "buy"},
#             {"indicator": "sma_10", "operator": "<", "value": "sma_50", "action": "sell"},
#         ],
#     },
#     {
#         "name": "On Balance Volume",
#         "conditions": [
#             {"indicator": "obv", "operator": "rising", "value": "", "action": "buy"},
#             {"indicator": "obv", "operator": "falling", "value": "", "action": "sell"},
#         ],
#     },
#     {
#         "name": "Parabolic SAR",
#         "conditions": [
#             {"indicator": "close", "operator": "crosses_above", "value": "sar", "action": "buy"},
#             {"indicator": "close", "operator": "crosses_below", "value": "sar", "action": "sell"},
#         ],
#     },
#     {
#         "name": "Pivot Points Standard",
#         "conditions": [
#             {"indicator": "close", "operator": ">", "value": "pivot", "action": "buy"},
#             {"indicator": "close", "operator": "<", "value": "pivot", "action": "sell"},
#         ],
#     },
#     {
#         "name": "Price Oscillator",
#         "conditions": [
#             {"indicator": "ppo", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "ppo", "operator": "<", "value": 0, "action": "sell"},
#         ],
#     },
#     {
#         "name": "Price Volume Trend",
#         "conditions": [
#             {"indicator": "pvt", "operator": "rising", "value": "", "action": "buy"},
#             {"indicator": "pvt", "operator": "falling", "value": "", "action": "sell"},
#         ],
#     },
#     {
#         "name": "Relative Strength Index (RSI)",
#         "conditions": [
#             {"indicator": "rsi", "operator": "<", "value": 30, "action": "buy"},
#             {"indicator": "rsi", "operator": ">", "value": 70, "action": "sell"},
#         ],
#     },
#     {
#         "name": "Smoothed Moving Average",
#         "conditions": [
#             {"indicator": "SMA", "operator": ">", "value": "SMA(prev)", "action": "buy"},
#             {"indicator": "SMA", "operator": "<", "value": "SMA(prev)", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Standard Deviation",
#         "conditions": [
#             {"indicator": "STDDEV", "operator": ">", "value": "20", "action": "buy"},
#             {"indicator": "STDDEV", "operator": "<", "value": "10", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Stochastic",
#         "conditions": [
#             {"indicator": "Stochastic", "operator": "<", "value": "20", "action": "buy"},
#             {"indicator": "Stochastic", "operator": ">", "value": "80", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Stochastic RSI",
#         "conditions": [
#             {"indicator": "StochRSI", "operator": "<", "value": "0.2", "action": "buy"},
#             {"indicator": "StochRSI", "operator": ">", "value": "0.8", "action": "sell"}
#         ]
#     },
#     {
#         "name": "SuperTrend",
#         "conditions": [
#             {"indicator": "Close", "operator": ">", "value": "SuperTrend", "action": "buy"},
#             {"indicator": "Close", "operator": "<", "value": "SuperTrend", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Spread",
#         "conditions": [
#             {"indicator": "Bid-Ask Spread", "operator": "<", "value": "0.05", "action": "buy"},
#             {"indicator": "Bid-Ask Spread", "operator": ">", "value": "0.1", "action": "sell"}
#         ]
#     },
#     {
#         "name": "TRIX",
#         "conditions": [
#             {"indicator": "TRIX", "operator": ">", "value": "0", "action": "buy"},
#             {"indicator": "TRIX", "operator": "<", "value": "0", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Triple EMA",
#         "conditions": [
#             {"indicator": "TEMA", "operator": ">", "value": "Close", "action": "buy"},
#             {"indicator": "TEMA", "operator": "<", "value": "Close", "action": "sell"}
#         ]
#     },
#     {
#         "name": "True Strength Indicator",
#         "conditions": [
#             {"indicator": "TSI", "operator": ">", "value": "0", "action": "buy"},
#             {"indicator": "TSI", "operator": "<", "value": "0", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Trend Strength Index",
#         "conditions": [
#             {"indicator": "TrendStrength", "operator": ">", "value": "20", "action": "buy"},
#             {"indicator": "TrendStrength", "operator": "<", "value": "-20", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Typical Price",
#         "conditions": [
#             {"indicator": "TypicalPrice", "operator": ">", "value": "SMA(TypicalPrice)", "action": "buy"},
#             {"indicator": "TypicalPrice", "operator": "<", "value": "SMA(TypicalPrice)", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Ultimate Oscillator",
#         "conditions": [
#             {"indicator": "UO", "operator": "<", "value": "30", "action": "buy"},
#             {"indicator": "UO", "operator": ">", "value": "70", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Volatility Close-to-Close",
#         "conditions": [
#             {"indicator": "VolatilityC2C", "operator": ">", "value": "20", "action": "buy"},
#             {"indicator": "VolatilityC2C", "operator": "<", "value": "10", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Volatility Zero Trend Close-to-Close",
#         "conditions": [
#             {"indicator": "VolatilityZTC2C", "operator": ">", "value": "15", "action": "buy"},
#             {"indicator": "VolatilityZTC2C", "operator": "<", "value": "10", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Volatility O-H-L-C",
#         "conditions": [
#             {"indicator": "VolatilityOHLC", "operator": ">", "value": "25", "action": "buy"},
#             {"indicator": "VolatilityOHLC", "operator": "<", "value": "15", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Volatility Index",
#         "conditions": [
#             {"indicator": "VIX", "operator": "<", "value": "20", "action": "buy"},
#             {"indicator": "VIX", "operator": ">", "value": "30", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Smoothed Moving Average",
#         "conditions": [
#             {"indicator": "SMA", "operator": ">", "value": "SMA(prev)", "action": "buy"},
#             {"indicator": "SMA", "operator": "<", "value": "SMA(prev)", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Standard Deviation",
#         "conditions": [
#             {"indicator": "STDDEV", "operator": ">", "value": "20", "action": "buy"},
#             {"indicator": "STDDEV", "operator": "<", "value": "10", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Stochastic",
#         "conditions": [
#             {"indicator": "Stochastic", "operator": "<", "value": "20", "action": "buy"},
#             {"indicator": "Stochastic", "operator": ">", "value": "80", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Stochastic RSI",
#         "conditions": [
#             {"indicator": "StochRSI", "operator": "<", "value": "0.2", "action": "buy"},
#             {"indicator": "StochRSI", "operator": ">", "value": "0.8", "action": "sell"}
#         ]
#     },
#     {
#         "name": "SuperTrend",
#         "conditions": [
#             {"indicator": "Close", "operator": ">", "value": "SuperTrend", "action": "buy"},
#             {"indicator": "Close", "operator": "<", "value": "SuperTrend", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Spread",
#         "conditions": [
#             {"indicator": "Bid-Ask Spread", "operator": "<", "value": "0.05", "action": "buy"},
#             {"indicator": "Bid-Ask Spread", "operator": ">", "value": "0.1", "action": "sell"}
#         ]
#     },
#     {
#         "name": "TRIX",
#         "conditions": [
#             {"indicator": "TRIX", "operator": ">", "value": "0", "action": "buy"},
#             {"indicator": "TRIX", "operator": "<", "value": "0", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Triple EMA",
#         "conditions": [
#             {"indicator": "TEMA", "operator": ">", "value": "Close", "action": "buy"},
#             {"indicator": "TEMA", "operator": "<", "value": "Close", "action": "sell"}
#         ]
#     },
#     {
#         "name": "True Strength Indicator",
#         "conditions": [
#             {"indicator": "TSI", "operator": ">", "value": "0", "action": "buy"},
#             {"indicator": "TSI", "operator": "<", "value": "0", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Trend Strength Index",
#         "conditions": [
#             {"indicator": "TrendStrength", "operator": ">", "value": "20", "action": "buy"},
#             {"indicator": "TrendStrength", "operator": "<", "value": "-20", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Typical Price",
#         "conditions": [
#             {"indicator": "TypicalPrice", "operator": ">", "value": "SMA(TypicalPrice)", "action": "buy"},
#             {"indicator": "TypicalPrice", "operator": "<", "value": "SMA(TypicalPrice)", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Ultimate Oscillator",
#         "conditions": [
#             {"indicator": "UO", "operator": "<", "value": "30", "action": "buy"},
#             {"indicator": "UO", "operator": ">", "value": "70", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Volatility Close-to-Close",
#         "conditions": [
#             {"indicator": "VolatilityC2C", "operator": ">", "value": "20", "action": "buy"},
#             {"indicator": "VolatilityC2C", "operator": "<", "value": "10", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Volatility Zero Trend Close-to-Close",
#         "conditions": [
#             {"indicator": "VolatilityZTC2C", "operator": ">", "value": "15", "action": "buy"},
#             {"indicator": "VolatilityZTC2C", "operator": "<", "value": "10", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Volatility O-H-L-C",
#         "conditions": [
#             {"indicator": "VolatilityOHLC", "operator": ">", "value": "25", "action": "buy"},
#             {"indicator": "VolatilityOHLC", "operator": "<", "value": "15", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Volatility Index",
#         "conditions": [
#             {"indicator": "VIX", "operator": "<", "value": "20", "action": "buy"},
#             {"indicator": "VIX", "operator": ">", "value": "30", "action": "sell"}
#         ]
#     }
#
# ]
# # premium 50 + 9 ==========================================================================================================
# PREDEFINED_STRATEGIES = [
#     {
#         "name": "LuxAlgo Signals & Overlays",
#         "conditions": [
#             {"indicator": "lux_k", "operator": ">", "value": 70, "action": "buy"},
#             {"indicator": "lux_k", "operator": "<", "value": 30, "action": "sell"}
#         ]
#     },
#     {
#         "name": "LuxAlgo Institutional",
#         "conditions": [
#             {"indicator": "institutional_flow", "operator": "==", "value": "buy", "action": "buy"},
#             {"indicator": "institutional_flow", "operator": "==", "value": "sell", "action": "sell"}
#         ]
#     },
#     {
#         "name": "LuxAlgo AI Backtester",
#         "conditions": [
#             {"indicator": "ai_signal", "operator": "==", "value": "buy", "action": "buy"},
#             {"indicator": "ai_signal", "operator": "==", "value": "sell", "action": "sell"}
#         ]
#     },
#     {
#         "name": "FluxCharts Premium Bundle",
#         "conditions": [
#             {"indicator": "flux_buy", "operator": "==", "value": True, "action": "buy"},
#             {"indicator": "flux_sell", "operator": "==", "value": True, "action": "sell"}
#         ]
#     },
#     {
#         "name": "Zeiierman Trend Range Detector",
#         "conditions": [
#             {"indicator": "trend_strength", "operator": ">", "value": 60, "action": "buy"},
#             {"indicator": "trend_strength", "operator": "<", "value": 40, "action": "sell"}
#         ]
#     },
#     {
#         "name": "Zeiierman Bollinger + Supertrend Hybrid Pro",
#         "conditions": [
#             {"indicator": "supertrend", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "bollinger_band_cross", "operator": "==", "value": "upper", "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime Complete Suite",
#         "conditions": [
#             {"indicator": "chartprime_signal", "operator": "==", "value": "buy", "action": "buy"},
#             {"indicator": "chartprime_signal", "operator": "==", "value": "sell", "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime Order Blocks Pro",
#         "conditions": [
#             {"indicator": "order_block", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "order_block", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime Momentum Divergence",
#         "conditions": [
#             {"indicator": "momentum_divergence", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "momentum_divergence", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime SMC Concepts Toolkit",
#         "conditions": [
#             {"indicator": "smc_break_structure", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "smc_break_structure", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "UltraAlgo Premium Indicator Pack",
#         "conditions": [
#             {"indicator": "ultraalgo_signal", "operator": "==", "value": "buy", "action": "buy"},
#             {"indicator": "ultraalgo_signal", "operator": "==", "value": "sell", "action": "sell"}
#         ]
#     },
#     {
#         "name": "BigBeluga Vol Profile Pro",
#         "conditions": [
#             {"indicator": "vol_profile_breakout", "operator": "==", "value": "up", "action": "buy"},
#             {"indicator": "vol_profile_breakout", "operator": "==", "value": "down", "action": "sell"}
#         ]
#     },
#     {
#         "name": "BigBeluga Momentum Divergence",
#         "conditions": [
#             {"indicator": "momentum_divergence", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "momentum_divergence", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "EliteAlgo Trend System",
#         "conditions": [
#             {"indicator": "elite_trend", "operator": "==", "value": "uptrend", "action": "buy"},
#             {"indicator": "elite_trend", "operator": "==", "value": "downtrend", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Market Cipher Premium",
#         "conditions": [
#             {"indicator": "cipher_b_wave", "operator": ">", "value": 60, "action": "buy"},
#             {"indicator": "cipher_b_wave", "operator": "<", "value": 40, "action": "sell"}
#         ]
#     },
#     {
#         "name": "WaveTrend Oscillator (LazyBear, paid version)",
#         "conditions": [
#             {"indicator": "wt_cross", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "wt_cross", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "CM_Ultimate RSI Multi Time Frame",
#         "conditions": [
#             {"indicator": "rsi_mtf", "operator": ">", "value": 60, "action": "buy"},
#             {"indicator": "rsi_mtf", "operator": "<", "value": 40, "action": "sell"}
#         ]
#     },
#     {
#         "name": "Death Cross Checker (50/200 MA)",
#         "conditions": [
#             {"indicator": "ma_cross", "operator": "==", "value": "golden", "action": "buy"},
#             {"indicator": "ma_cross", "operator": "==", "value": "death", "action": "sell"}
#         ]
#     },
#     {
#         "name": "TDI – Traders Dynamic Index (Goldminds)",
#         "conditions": [
#             {"indicator": "tdi_cross", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "tdi_cross", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "True Strength Index (Premium version)",
#         "conditions": [
#             {"indicator": "tsi_cross", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "tsi_cross", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "FluxCharts Smart Money Concepts",
#         "conditions": [
#             {"indicator": "supply_demand_zone", "operator": "==", "value": "demand", "action": "buy"},
#             {"indicator": "supply_demand_zone", "operator": "==", "value": "supply", "action": "sell"}
#         ]
#     },
#     {
#         "name": "FluxCharts Liquidity & Order Blocks",
#         "conditions": [
#             {"indicator": "liquidity_zone", "operator": "==", "value": "below_price", "action": "buy"},
#             {"indicator": "order_block", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Zeiierman SuperTrend Pro",
#         "conditions": [
#             {"indicator": "supertrend_signal", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "supertrend_signal", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "LuxAlgo Price Action Concepts",
#         "conditions": [
#             {"indicator": "bullish_engulfing", "operator": "==", "value": True, "action": "buy"},
#             {"indicator": "bearish_engulfing", "operator": "==", "value": True, "action": "sell"}
#         ]
#     },
#     {
#         "name": "LuxAlgo Liquidity Zones",
#         "conditions": [
#             {"indicator": "liquidity_zone_proximity", "operator": "<=", "value": 0.5, "action": "buy"},
#             {"indicator": "liquidity_zone_proximity", "operator": "<=", "value": 0.5, "action": "sell"}
#         ]
#     },
#     {
#         "name": "LuxAlgo Zone Strength Gauge",
#         "conditions": [
#             {"indicator": "zone_strength", "operator": ">=", "value": 75, "action": "buy"},
#             {"indicator": "zone_strength", "operator": "<=", "value": 25, "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime Reversal Patterns Suite",
#         "conditions": [
#             {"indicator": "reversal_pattern", "operator": "in", "value": ["double_bottom", "inverse_head_shoulders"], "action": "buy"},
#             {"indicator": "reversal_pattern", "operator": "in", "value": ["double_top", "head_shoulders"], "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime Trend Strength Dashboard",
#         "conditions": [
#             {"indicator": "trend_strength", "operator": ">=", "value": 80, "action": "buy"},
#             {"indicator": "trend_strength", "operator": "<=", "value": 20, "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime Pivot Zone Master",
#         "conditions": [
#             {"indicator": "price_vs_pivot", "operator": "==", "value": "above", "action": "buy"},
#             {"indicator": "price_vs_pivot", "operator": "==", "value": "below", "action": "sell"}
#         ]
#     },
#     {
#         "name": "UltraAlgo Correlation Indicator",
#         "conditions": [
#             {"indicator": "correlation_with_index", "operator": ">", "value": 0.8, "action": "buy"},
#             {"indicator": "correlation_with_index", "operator": "<", "value": -0.8, "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime Daily Market Map",
#         "conditions": [
#             {"indicator": "MarketMapSignal", "operator": "==", "value": "DailyBuyZone", "action": "buy"},
#             {"indicator": "MarketMapSignal", "operator": "==", "value": "DailySellZone", "action": "sell"}
#         ]
#     },
#     {
#         "name": "BigBeluga Order Flow Tracker",
#         "conditions": [
#             {"indicator": "OrderFlowDelta", "operator": ">", "value": 0, "action": "buy"},
#             {"indicator": "OrderFlowDelta", "operator": "<", "value": 0, "action": "sell"}
#         ]
#     },
#     {
#         "name": "UltraAlgo VWAP Trend System",
#         "conditions": [
#             {"indicator": "Price", "operator": ">", "value": "VWAP", "action": "buy"},
#             {"indicator": "Price", "operator": "<", "value": "VWAP", "action": "sell"}
#         ]
#     },
#     {
#         "name": "UltraAlgo Adaptive MA Suite",
#         "conditions": [
#             {"indicator": "Price", "operator": "crossesAbove", "value": "AdaptiveMA", "action": "buy"},
#             {"indicator": "Price", "operator": "crossesBelow", "value": "AdaptiveMA", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Zeiierman Range Breakout Bars",
#         "conditions": [
#             {"indicator": "RangeBreakout", "operator": "==", "value": "UpBreak", "action": "buy"},
#             {"indicator": "RangeBreakout", "operator": "==", "value": "DownBreak", "action": "sell"}
#         ]
#     },
#     {
#         "name": "FluxCharts Smart Stops & Targets",
#         "conditions": [
#             {"indicator": "SmartEntry", "operator": "==", "value": "EntrySignal", "action": "buy"},
#             {"indicator": "SmartExit", "operator": "==", "value": "ExitSignal", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Market Cipher AI Alerts",
#         "conditions": [
#             {"indicator": "CipherAI", "operator": "==", "value": "GreenDot", "action": "buy"},
#             {"indicator": "CipherAI", "operator": "==", "value": "RedDot", "action": "sell"}
#         ]
#     },
#     {
#         "name": "LuxAlgo Dynamic Price Levels",
#         "conditions": [
#             {"indicator": "Price", "operator": "crossesAbove", "value": "DynamicSupport", "action": "buy"},
#             {"indicator": "Price", "operator": "crossesBelow", "value": "DynamicResistance", "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime Volume Profile Vault",
#         "conditions": [
#             {"indicator": "Price", "operator": ">", "value": "POC", "action": "buy"},
#             {"indicator": "Price", "operator": "<", "value": "POC", "action": "sell"}
#         ]
#     },
#     {
#         "name": "BigBeluga Trend Filter Premium",
#         "conditions": [
#             {"indicator": "TrendFilter", "operator": "==", "value": "Bullish", "action": "buy"},
#             {"indicator": "TrendFilter", "operator": "==", "value": "Bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "UltraAlgo Pattern Recognition AI",
#         "conditions": [
#             {"indicator": "candle_pattern_ultraalgo", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "candle_pattern_ultraalgo", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "BigBeluga Divergence Scanner",
#         "conditions": [
#             {"indicator": "rsi_divergence", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "rsi_divergence", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Market Cipher A (version II)",
#         "conditions": [
#             {"indicator": "cipher_a_symbol", "operator": "==", "value": "green_dot", "action": "buy"},
#             {"indicator": "cipher_a_symbol", "operator": "==", "value": "red_dot", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Market Cipher B (version II)",
#         "conditions": [
#             {"indicator": "wave_trend_cross", "operator": "==", "value": "bullish", "action": "buy"},
#             {"indicator": "wave_trend_cross", "operator": "==", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "EliteAlgo AI Trend Detector",
#         "conditions": [
#             {"indicator": "elite_trend", "operator": "==", "value": "buy_signal", "action": "buy"},
#             {"indicator": "elite_trend", "operator": "==", "value": "sell_signal", "action": "sell"}
#         ]
#     },
#     {
#         "name": "FluxCharts Multi-Timeframe Engine",
#         "conditions": [
#             {"indicator": "multi_tf_trend", "operator": "==", "value": "aligned_up", "action": "buy"},
#             {"indicator": "multi_tf_trend", "operator": "==", "value": "aligned_down", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Zeiierman Volatility Squeeze Detector",
#         "conditions": [
#             {"indicator": "squeeze_breakout", "operator": "==", "value": "up", "action": "buy"},
#             {"indicator": "squeeze_breakout", "operator": "==", "value": "down", "action": "sell"}
#         ]
#     },
#     {
#         "name": "LuxAlgo Breakout Bands",
#         "conditions": [
#             {"indicator": "price_above_upper_band", "operator": "==", "value": True, "action": "buy"},
#             {"indicator": "price_below_lower_band", "operator": "==", "value": True, "action": "sell"}
#         ]
#     },
#     {
#         "name": "LuxAlgo RSI Heatmap (premium)",
#         "conditions": [
#             {"indicator": "rsi_heatmap_color", "operator": "==", "value": "green", "action": "buy"},
#             {"indicator": "rsi_heatmap_color", "operator": "==", "value": "red", "action": "sell"}
#         ]
#     },
#     {
#         "name": "ChartPrime Scalp Signal Alerts",
#         "conditions": [
#             {"indicator": "scalp_signal", "operator": "==", "value": "long", "action": "buy"},
#             {"indicator": "scalp_signal", "operator": "==", "value": "short", "action": "sell"}
#         ]
#     },
#     # Other 9====================================================================================
#     {
#         "name": "Swing & Scalp Trading Signals",
#         "conditions": [
#             {"indicator": "ema_20", "operator": "crosses_above", "value": "ema_50", "action": "buy"},
#             {"indicator": "ema_20", "operator": "crosses_below", "value": "ema_50", "action": "sell"}
#         ]
#     },
#     {
#         "name": "1 Minute Scalping Indicator (Trend Friend)",
#         "conditions": [
#             {"indicator": "rsi", "operator": "lt", "value": 30, "action": "buy"},
#             {"indicator": "rsi", "operator": "gt", "value": 70, "action": "sell"}
#         ]
#     },
#     {
#         "name": "Volume Spike Levels (Trend Friend)",
#         "conditions": [
#             {"indicator": "volume", "operator": "gt", "value": "sma_volume_20 * 2", "action": "buy"},
#             {"indicator": "volume", "operator": "lt", "value": "sma_volume_20", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Support And Resistance (Trend Friend)",
#         "conditions": [
#             {"indicator": "close", "operator": "crosses_above", "value": "support_level", "action": "buy"},
#             {"indicator": "close", "operator": "crosses_below", "value": "resistance_level", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Pi Cycle Bottom Indicator",
#         "conditions": [
#             {"indicator": "ema_111", "operator": "crosses_above", "value": "sma_350", "action": "buy"},
#             {"indicator": "ema_111", "operator": "crosses_below", "value": "sma_350", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Gaps Indicator (Premium)",
#         "conditions": [
#             {"indicator": "gap_up", "operator": "eq", "value": True, "action": "buy"},
#             {"indicator": "gap_down", "operator": "eq", "value": True, "action": "sell"}
#         ]
#     },
#     {
#         "name": "RCI3lines by Gero",
#         "conditions": [
#             {"indicator": "rci_short", "operator": "lt", "value": -80, "action": "buy"},
#             {"indicator": "rci_short", "operator": "gt", "value": 80, "action": "sell"}
#         ]
#     },
#     {
#         "name": "WaveTrend Oscillator (LazyBear)",
#         "conditions": [
#             {"indicator": "wt_cross", "operator": "eq", "value": "bullish", "action": "buy"},
#             {"indicator": "wt_cross", "operator": "eq", "value": "bearish", "action": "sell"}
#         ]
#     },
#     {
#         "name": "Gaps Indicator (Basic)",
#         "conditions": [
#             {"indicator": "gap_detected", "operator": "eq", "value": True, "action": "buy"},
#             {"indicator": "gap_filled", "operator": "eq", "value": True, "action": "sell"}
#         ]
#     }
# ]





# PREDEFINED_STRATEGIES = [
#
#     {
#         "name": "RSI Oversold",
#         "conditions": [
#             {
#                 "indicator": "rsi",
#                 "operator": "<",
#                 "value": "30"
#             }
#         ],
#         "action": "buy"
#     },
#
#     {
#         "name": "EMA Crossover",
#         "conditions": [
#             {
#                 "indicator": "ema20",
#                 "operator": "crosses_above",
#                 "value": "ema50"
#             }
#         ],
#         "action": "buy"
#     },
#
#     {
#         "name": "MACD Bullish",
#         "conditions": [
#             {
#                 "indicator": "macd",
#                 "operator": ">",
#                 "value": "0"
#             }
#         ],
#         "action": "buy"
#     },
#
#     {
#         "name": "ADX Strong Trend",
#         "conditions": [
#             {
#                 "indicator": "adx",
#                 "operator": ">",
#                 "value": "25"
#             }
#         ],
#         "action": "buy"
#     },
#
#     {
#         "name": "Bollinger Rebound",
#         "conditions": [
#             {
#                 "indicator": "close",
#                 "operator": "<",
#                 "value": "bollinger_lower"
#             }
#         ],
#         "action": "buy"
#     }
#
# ]


