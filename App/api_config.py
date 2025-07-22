# USE_MT5 = True
# MT5_LOGIN = 480920
# MT5_PASSWORD = "V*TbWo8i"
# MT5_SERVER = "ICMCapitalLtd-Demo"

# ------------------------------------------------For Testing
DEFAULT_MT5_LOGIN = 480920
DEFAULT_MT5_PASSWORD = "V*TbWo8i"
DEFAULT_MT5_SERVER = "ICMCapitalLtd-Demo"


dynamic_mt5_credentials = {
    "login": DEFAULT_MT5_LOGIN,
    "password": DEFAULT_MT5_PASSWORD,
    "server": DEFAULT_MT5_SERVER,
}
# -----------------------------------------------------For Testing

# -----------------------------------------------------for production
# dynamic_mt5_credentials = {
#     "login": None,
#     "password": None,
#     "server": None,
# }

# These are the variables used in other files
MT5_LOGIN = lambda: dynamic_mt5_credentials["login"]
MT5_PASSWORD = lambda: dynamic_mt5_credentials["password"]
MT5_SERVER = lambda: dynamic_mt5_credentials["server"]


def set_user_credentials(login: int, password: str, server: str):
    dynamic_mt5_credentials["login"] = login
    dynamic_mt5_credentials["password"] = password
    dynamic_mt5_credentials["server"] = server