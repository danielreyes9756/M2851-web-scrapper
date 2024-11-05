import random
from src.constants import USER_AGENTS, PROXIES


def get_random_headers():
    """Return random agent configuration."""
    return {'User-Agent': random.choice(USER_AGENTS)}


def get_random_proxy():
    """Return random proxy configuration."""
    return random.choice(PROXIES)
