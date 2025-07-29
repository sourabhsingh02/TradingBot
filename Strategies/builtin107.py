    # {
    #     "name": "52 Week High/Low",
    #     "conditions": [
    #         {"indicator": "price", "operator": "crosses_above", "value": "52_week_high", "action": "buy"},
    #         {"indicator": "price", "operator": "crosses_below", "value": "52_week_low", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Accelerator Oscillator",
    #     "conditions": [
    #         {"indicator": "ac", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "ac", "operator": "<", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Accumulation/Distribution",
    #     "conditions": [
    #         {"indicator": "ad", "operator": "increasing", "value": "", "action": "buy"},
    #         {"indicator": "ad", "operator": "decreasing", "value": "", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Accumulative Swing Index",
    #     "conditions": [
    #         {"indicator": "asi", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "asi", "operator": "<", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Advance/Decline",
    #     "conditions": [
    #         {"indicator": "adv_dec", "operator": ">", "value": "threshold", "action": "buy"},
    #         {"indicator": "adv_dec", "operator": "<", "value": "threshold", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Arnaud Legoux Moving Average",
    #     "conditions": [
    #         {"indicator": "alma", "operator": "crosses_above", "value": "price", "action": "buy"},
    #         {"indicator": "alma", "operator": "crosses_below", "value": "price", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Aroon",
    #     "conditions": [
    #         {"indicator": "aroon_up", "operator": ">", "value": 70, "action": "buy"},
    #         {"indicator": "aroon_down", "operator": ">", "value": 70, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Average Directional Index",
    #     "conditions": [
    #         {"indicator": "adx", "operator": ">", "value": 25, "action": "buy"},
    #         {"indicator": "adx", "operator": "<", "value": 20, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Average Price",
    #     "conditions": [
    #         {"indicator": "price", "operator": ">", "value": "average_price", "action": "buy"},
    #         {"indicator": "price", "operator": "<", "value": "average_price", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Average True Range",
    #     "conditions": [
    #         {"indicator": "atr", "operator": "rising", "value": "", "action": "buy"},
    #         {"indicator": "atr", "operator": "falling", "value": "", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Awesome Oscillator",
    #     "conditions": [
    #         {"indicator": "ao", "operator": "crosses_above", "value": 0, "action": "buy"},
    #         {"indicator": "ao", "operator": "crosses_below", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Balance of Power",
    #     "conditions": [
    #         {"indicator": "bop", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "bop", "operator": "<", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Bollinger Bands",
    #     "conditions": [
    #         {"indicator": "price", "operator": "crosses_below", "value": "lower_band", "action": "buy"},
    #         {"indicator": "price", "operator": "crosses_above", "value": "upper_band", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Bollinger Bands %B",
    #     "conditions": [
    #         {"indicator": "bb_percent", "operator": "<", "value": 0, "action": "buy"},
    #         {"indicator": "bb_percent", "operator": ">", "value": 1, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Bollinger Bands Width",
    #     "conditions": [
    #         {"indicator": "bb_width", "operator": "increasing", "value": "", "action": "buy"},
    #         {"indicator": "bb_width", "operator": "decreasing", "value": "", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Chaikin Money Flow",
    #     "conditions": [
    #         {"indicator": "cmf", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "cmf", "operator": "<", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Chaikin Oscillator",
    #     "conditions": [
    #         {"indicator": "cho", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "cho", "operator": "<", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Chaikin Volatility",
    #     "conditions": [
    #         {"indicator": "chaikin_vol", "operator": ">", "value": "threshold", "action": "buy"},
    #         {"indicator": "chaikin_vol", "operator": "<", "value": "threshold", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Chande Kroll Stop",
    #     "conditions": [
    #         {"indicator": "price", "operator": "crosses_above", "value": "ck_stop", "action": "buy"},
    #         {"indicator": "price", "operator": "crosses_below", "value": "ck_stop", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Chande Momentum Oscillator",
    #     "conditions": [
    #         {"indicator": "cmo", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "cmo", "operator": "<", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Double EMA",
    #     "conditions": [
    #         {"indicator": "DEMA", "operator": ">", "value": "price", "action": "buy"},
    #         {"indicator": "DEMA", "operator": "<", "value": "price", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Ease of Movement",
    #     "conditions": [
    #         {"indicator": "EOM", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "EOM", "operator": "<", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Elder's Force Index",
    #     "conditions": [
    #         {"indicator": "EFI", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "EFI", "operator": "<", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "EMA Cross",
    #     "conditions": [
    #         {"indicator": "EMA_9", "operator": "crosses_above", "value": "EMA_21", "action": "buy"},
    #         {"indicator": "EMA_9", "operator": "crosses_below", "value": "EMA_21", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Envelopes",
    #     "conditions": [
    #         {"indicator": "price", "operator": "<", "value": "LowerEnvelope", "action": "buy"},
    #         {"indicator": "price", "operator": ">", "value": "UpperEnvelope", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Fisher Transform",
    #     "conditions": [
    #         {"indicator": "Fisher", "operator": "crosses_above", "value": 0, "action": "buy"},
    #         {"indicator": "Fisher", "operator": "crosses_below", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Guppy Multiple Moving Average",
    #     "conditions": [
    #         {"indicator": "ShortGuppy", "operator": ">", "value": "LongGuppy", "action": "buy"},
    #         {"indicator": "ShortGuppy", "operator": "<", "value": "LongGuppy", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Historical Volatility",
    #     "conditions": [
    #         {"indicator": "HistoricalVolatility", "operator": ">", "value": 1.5, "action": "buy"},
    #         {"indicator": "HistoricalVolatility", "operator": "<", "value": 1.0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Hull Moving Average",
    #     "conditions": [
    #         {"indicator": "HMA", "operator": ">", "value": "price", "action": "buy"},
    #         {"indicator": "HMA", "operator": "<", "value": "price", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Ichimoku Cloud",
    #     "conditions": [
    #         {"indicator": "price", "operator": ">", "value": "CloudTop", "action": "buy"},
    #         {"indicator": "price", "operator": "<", "value": "CloudBottom", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Keltner Channels",
    #     "conditions": [
    #         {"indicator": "price", "operator": "<", "value": "LowerKC", "action": "buy"},
    #         {"indicator": "price", "operator": ">", "value": "UpperKC", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Klinger Oscillator",
    #     "conditions": [
    #         {"indicator": "Klinger", "operator": "crosses_above", "value": "Signal", "action": "buy"},
    #         {"indicator": "Klinger", "operator": "crosses_below", "value": "Signal", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Know Sure Thing",
    #     "conditions": [
    #         {"indicator": "KST", "operator": ">", "value": "Signal", "action": "buy"},
    #         {"indicator": "KST", "operator": "<", "value": "Signal", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Least Squares Moving Average",
    #     "conditions": [
    #         {"indicator": "LSMA", "operator": "crosses_above", "value": "price", "action": "buy"},
    #         {"indicator": "LSMA", "operator": "crosses_below", "value": "price", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Linear Regression Curve",
    #     "conditions": [
    #         {"indicator": "price", "operator": ">", "value": "LinRegCurve", "action": "buy"},
    #         {"indicator": "price", "operator": "<", "value": "LinRegCurve", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Linear Regression Slope",
    #     "conditions": [
    #         {"indicator": "LinRegSlope", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "LinRegSlope", "operator": "<", "value": 0, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "MA Cross",
    #     "conditions": [
    #         {"indicator": "MA_10", "operator": "crosses_above", "value": "MA_20", "action": "buy"},
    #         {"indicator": "MA_10", "operator": "crosses_below", "value": "MA_20", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "MA with EMA Cross",
    #     "conditions": [
    #         {"indicator": "MA", "operator": "crosses_above", "value": "EMA", "action": "buy"},
    #         {"indicator": "MA", "operator": "crosses_below", "value": "EMA", "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "Mass Index",
    #     "conditions": [
    #         {"indicator": "MassIndex", "operator": "crosses_above", "value": 27, "action": "buy"},
    #         {"indicator": "MassIndex", "operator": "crosses_below", "value": 26.5, "action": "sell"},
    #     ]
    # },
    # {
    #     "name": "McGinley Dynamic",
    #     "conditions": [
    #         {"indicator": "price", "operator": "crosses_above", "value": "McGinley", "action": "buy"},
    #         {"indicator": "price", "operator": "crosses_below", "value": "McGinley", "action": "sell"},
    #     ]
    # }
    #
    # {
    #     "name": "Momentum Oscillator",
    #     "conditions": [
    #         {"indicator": "momentum", "operator": ">", "value": 100, "action": "buy"},
    #         {"indicator": "momentum", "operator": "<", "value": 100, "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Money Flow Index",
    #     "conditions": [
    #         {"indicator": "mfi", "operator": "<", "value": 20, "action": "buy"},
    #         {"indicator": "mfi", "operator": ">", "value": 80, "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Moving Average",
    #     "conditions": [
    #         {"indicator": "close", "operator": ">", "value": "sma_50", "action": "buy"},
    #         {"indicator": "close", "operator": "<", "value": "sma_50", "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Moving Average Exponential",
    #     "conditions": [
    #         {"indicator": "close", "operator": ">", "value": "ema_50", "action": "buy"},
    #         {"indicator": "close", "operator": "<", "value": "ema_50", "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Moving Average Weighted",
    #     "conditions": [
    #         {"indicator": "close", "operator": ">", "value": "wma_50", "action": "buy"},
    #         {"indicator": "close", "operator": "<", "value": "wma_50", "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Moving Average Ribbon",
    #     "conditions": [
    #         {"indicator": "sma_10", "operator": ">", "value": "sma_50", "action": "buy"},
    #         {"indicator": "sma_10", "operator": "<", "value": "sma_50", "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "On Balance Volume",
    #     "conditions": [
    #         {"indicator": "obv", "operator": "rising", "value": "", "action": "buy"},
    #         {"indicator": "obv", "operator": "falling", "value": "", "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Parabolic SAR",
    #     "conditions": [
    #         {"indicator": "close", "operator": "crosses_above", "value": "sar", "action": "buy"},
    #         {"indicator": "close", "operator": "crosses_below", "value": "sar", "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Pivot Points Standard",
    #     "conditions": [
    #         {"indicator": "close", "operator": ">", "value": "pivot", "action": "buy"},
    #         {"indicator": "close", "operator": "<", "value": "pivot", "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Price Oscillator",
    #     "conditions": [
    #         {"indicator": "ppo", "operator": ">", "value": 0, "action": "buy"},
    #         {"indicator": "ppo", "operator": "<", "value": 0, "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Price Volume Trend",
    #     "conditions": [
    #         {"indicator": "pvt", "operator": "rising", "value": "", "action": "buy"},
    #         {"indicator": "pvt", "operator": "falling", "value": "", "action": "sell"},
    #     ],
    # },
    # {
    #     "name": "Relative Strength Index (RSI)",
    #     "conditions": [
    #         {"indicator": "rsi", "operator": "<", "value": 30, "action": "buy"},
    #         {"indicator": "rsi", "operator": ">", "value": 70, "action": "sell"},
    #     ],
    # },
    #
    #
    # {
    #     "name": "Smoothed Moving Average",
    #     "conditions": [
    #         {"indicator": "SMA", "operator": ">", "value": "SMA(prev)", "action": "buy"},
    #         {"indicator": "SMA", "operator": "<", "value": "SMA(prev)", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Standard Deviation",
    #     "conditions": [
    #         {"indicator": "STDDEV", "operator": ">", "value": "20", "action": "buy"},
    #         {"indicator": "STDDEV", "operator": "<", "value": "10", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Stochastic",
    #     "conditions": [
    #         {"indicator": "Stochastic", "operator": "<", "value": "20", "action": "buy"},
    #         {"indicator": "Stochastic", "operator": ">", "value": "80", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Stochastic RSI",
    #     "conditions": [
    #         {"indicator": "StochRSI", "operator": "<", "value": "0.2", "action": "buy"},
    #         {"indicator": "StochRSI", "operator": ">", "value": "0.8", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "SuperTrend",
    #     "conditions": [
    #         {"indicator": "Close", "operator": ">", "value": "SuperTrend", "action": "buy"},
    #         {"indicator": "Close", "operator": "<", "value": "SuperTrend", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Spread",
    #     "conditions": [
    #         {"indicator": "Bid-Ask Spread", "operator": "<", "value": "0.05", "action": "buy"},
    #         {"indicator": "Bid-Ask Spread", "operator": ">", "value": "0.1", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "TRIX",
    #     "conditions": [
    #         {"indicator": "TRIX", "operator": ">", "value": "0", "action": "buy"},
    #         {"indicator": "TRIX", "operator": "<", "value": "0", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Triple EMA",
    #     "conditions": [
    #         {"indicator": "TEMA", "operator": ">", "value": "Close", "action": "buy"},
    #         {"indicator": "TEMA", "operator": "<", "value": "Close", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "True Strength Indicator",
    #     "conditions": [
    #         {"indicator": "TSI", "operator": ">", "value": "0", "action": "buy"},
    #         {"indicator": "TSI", "operator": "<", "value": "0", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Trend Strength Index",
    #     "conditions": [
    #         {"indicator": "TrendStrength", "operator": ">", "value": "20", "action": "buy"},
    #         {"indicator": "TrendStrength", "operator": "<", "value": "-20", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Typical Price",
    #     "conditions": [
    #         {"indicator": "TypicalPrice", "operator": ">", "value": "SMA(TypicalPrice)", "action": "buy"},
    #         {"indicator": "TypicalPrice", "operator": "<", "value": "SMA(TypicalPrice)", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Ultimate Oscillator",
    #     "conditions": [
    #         {"indicator": "UO", "operator": "<", "value": "30", "action": "buy"},
    #         {"indicator": "UO", "operator": ">", "value": "70", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Volatility Close-to-Close",
    #     "conditions": [
    #         {"indicator": "VolatilityC2C", "operator": ">", "value": "20", "action": "buy"},
    #         {"indicator": "VolatilityC2C", "operator": "<", "value": "10", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Volatility Zero Trend Close-to-Close",
    #     "conditions": [
    #         {"indicator": "VolatilityZTC2C", "operator": ">", "value": "15", "action": "buy"},
    #         {"indicator": "VolatilityZTC2C", "operator": "<", "value": "10", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Volatility O-H-L-C",
    #     "conditions": [
    #         {"indicator": "VolatilityOHLC", "operator": ">", "value": "25", "action": "buy"},
    #         {"indicator": "VolatilityOHLC", "operator": "<", "value": "15", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Volatility Index",
    #     "conditions": [
    #         {"indicator": "VIX", "operator": "<", "value": "20", "action": "buy"},
    #         {"indicator": "VIX", "operator": ">", "value": "30", "action": "sell"}
    #     ]
    # }
    #
    #
    # {
    #     "name": "Smoothed Moving Average",
    #     "conditions": [
    #         {"indicator": "SMA", "operator": ">", "value": "SMA(prev)", "action": "buy"},
    #         {"indicator": "SMA", "operator": "<", "value": "SMA(prev)", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Standard Deviation",
    #     "conditions": [
    #         {"indicator": "STDDEV", "operator": ">", "value": "20", "action": "buy"},
    #         {"indicator": "STDDEV", "operator": "<", "value": "10", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Stochastic",
    #     "conditions": [
    #         {"indicator": "Stochastic", "operator": "<", "value": "20", "action": "buy"},
    #         {"indicator": "Stochastic", "operator": ">", "value": "80", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Stochastic RSI",
    #     "conditions": [
    #         {"indicator": "StochRSI", "operator": "<", "value": "0.2", "action": "buy"},
    #         {"indicator": "StochRSI", "operator": ">", "value": "0.8", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "SuperTrend",
    #     "conditions": [
    #         {"indicator": "Close", "operator": ">", "value": "SuperTrend", "action": "buy"},
    #         {"indicator": "Close", "operator": "<", "value": "SuperTrend", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Spread",
    #     "conditions": [
    #         {"indicator": "Bid-Ask Spread", "operator": "<", "value": "0.05", "action": "buy"},
    #         {"indicator": "Bid-Ask Spread", "operator": ">", "value": "0.1", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "TRIX",
    #     "conditions": [
    #         {"indicator": "TRIX", "operator": ">", "value": "0", "action": "buy"},
    #         {"indicator": "TRIX", "operator": "<", "value": "0", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Triple EMA",
    #     "conditions": [
    #         {"indicator": "TEMA", "operator": ">", "value": "Close", "action": "buy"},
    #         {"indicator": "TEMA", "operator": "<", "value": "Close", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "True Strength Indicator",
    #     "conditions": [
    #         {"indicator": "TSI", "operator": ">", "value": "0", "action": "buy"},
    #         {"indicator": "TSI", "operator": "<", "value": "0", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Trend Strength Index",
    #     "conditions": [
    #         {"indicator": "TrendStrength", "operator": ">", "value": "20", "action": "buy"},
    #         {"indicator": "TrendStrength", "operator": "<", "value": "-20", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Typical Price",
    #     "conditions": [
    #         {"indicator": "TypicalPrice", "operator": ">", "value": "SMA(TypicalPrice)", "action": "buy"},
    #         {"indicator": "TypicalPrice", "operator": "<", "value": "SMA(TypicalPrice)", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Ultimate Oscillator",
    #     "conditions": [
    #         {"indicator": "UO", "operator": "<", "value": "30", "action": "buy"},
    #         {"indicator": "UO", "operator": ">", "value": "70", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Volatility Close-to-Close",
    #     "conditions": [
    #         {"indicator": "VolatilityC2C", "operator": ">", "value": "20", "action": "buy"},
    #         {"indicator": "VolatilityC2C", "operator": "<", "value": "10", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Volatility Zero Trend Close-to-Close",
    #     "conditions": [
    #         {"indicator": "VolatilityZTC2C", "operator": ">", "value": "15", "action": "buy"},
    #         {"indicator": "VolatilityZTC2C", "operator": "<", "value": "10", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Volatility O-H-L-C",
    #     "conditions": [
    #         {"indicator": "VolatilityOHLC", "operator": ">", "value": "25", "action": "buy"},
    #         {"indicator": "VolatilityOHLC", "operator": "<", "value": "15", "action": "sell"}
    #     ]
    # },
    # {
    #     "name": "Volatility Index",
    #     "conditions": [
    #         {"indicator": "VIX", "operator": "<", "value": "20", "action": "buy"},
    #         {"indicator": "VIX", "operator": ">", "value": "30", "action": "sell"}
    #     ]
    # }
