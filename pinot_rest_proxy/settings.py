import os


def bool_env(name, default: bool = False):
    value = os.environ.get(name, default)
    if value in ("False", "false", "0"):
        return False
    return bool(value)


def float_env(name, default: float = 0.0):
    return float(os.environ.get(name, default))


def int_env(name, default: int = 0):
    return int(os.environ.get(name, default))


def str_env(name, default: str = ""):
    return os.environ.get(name, default)


# Whether or not Pinot Rest Proxy is run in debug mode.
# Never run Pinot Rest Proxy in debug mode outside of development!
DEBUG = bool_env("DEBUG", False)

# The host the ASGI app should use.
HOST = str_env("HOST", "0.0.0.0")

# The port the ASGI app should use
PORT = int_env("PORT", 8000)

# URL of Pinot URL used to fetch metadata about Tenants and Brokers.
PINOT_CONTROLLER_URL = str_env("PINOT_CONTROLLER_URL")

# Interval in seconds to refresh tenants and broker list
# This interval should be big enough to not put to much pressure on Pinot Controller
# but low enough to refresh proxy quickly when tenant is created / updated / deleted.
ROUTING_REFRESH_INTERVAL = int_env("ROUTING_REFRESH_INTERVAL", 120)
