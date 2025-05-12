import random

PROXY_LIST = [
    "http://user:pass@resproxy1.com:8000",
    "http://user:pass@resproxy2.com:8000"
]

def get_random_proxy():
    return random.choice(PROXY_LIST)
