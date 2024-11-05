import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from src.logic.config import get_random_headers, get_random_proxy


def __setup_driver(proxy=None):
    chrome_options = Options()

    # Todo: Reyes, under review.
    # if proxy:
        # chrome_options.add_argument(f'--proxy-server={proxy}')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument(f'user-agent={get_random_headers()["User-Agent"]}')

    # Todo: Reyes, tmp solution.
    service = ChromeService(executable_path='C:/Users/danie/Downloads/chromedriver-win64/chromedriver.exe')
    return webdriver.Chrome(service=service, options=chrome_options)


def try_setup_with_proxy(url):
    """Tries to set up the driver with a working proxy. Falls back to no proxy if all fail."""
    for attempt in range(3):
        proxy = get_random_proxy()
        try:
            # We should use proxy (see above) but this one works!
            # Todo: Reyes, tmp solution.
            driver = __setup_driver(proxy=proxy)
            driver.get(url)
            if driver.title:
                # print(f"Connected successfully with proxy {proxy}")
                return driver
        except Exception as e:
            print(f"Proxy failed ({proxy}): {e}")
        time.sleep(2)
    print("No working proxy found, proceeding without proxy.")
    return __setup_driver()
