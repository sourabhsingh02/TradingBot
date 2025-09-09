
dynamic_mt5_credentials = {
    "login": None,
    "password": None,
    "server": None,
}

# These are the variables used in other files
MT5_LOGIN = lambda: dynamic_mt5_credentials["login"]
MT5_PASSWORD = lambda: dynamic_mt5_credentials["password"]
MT5_SERVER = lambda: dynamic_mt5_credentials["server"]


def set_user_credentials(login: int, password: str, server: str):
    dynamic_mt5_credentials["login"] = login
    dynamic_mt5_credentials["password"] = password
    dynamic_mt5_credentials["server"] = server