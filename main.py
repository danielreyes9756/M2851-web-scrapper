import re
import time
import random
import requests
from bs4 import BeautifulSoup
from requests import RequestException

# List of user agents from https://www.whatismybrowser.com/guides/the-latest-user-agent/.
user_agents = [
    'Mozilla/5.0 (X11; CrOS x86_64 15917.71.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.132 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS armv7l 15917.71.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.132 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14.7; rv:132.0) Gecko/20100101 Firefox/132.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_7_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Safari/605.1.15',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (iPad; CPU OS 17_7_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/18.0 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Vivaldi/7.0.3495.10',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Vivaldi/7.0.3495.10',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 Edg/130.0.2849.68'
]

# List of proxies from https://free-proxy-list.net/.
proxies = [
    'https://8.219.97.248:80',  # Singapore
    'https://200.174.198.86:8888',  # Brazil
    'https://20.111.54.16:8123',  # France
    'https://222.252.194.29:8080',  # Vietnam
    'http://157.254.53.50:80',  # Hong Kong
    'https://160.86.242.23:8080',  # Hong Kong
    'http://198.44.255.5:80',  # United States
    'http://77.221.139.76:8080',  # Sweeden
    'http://41.59.90.171:80',  # Tanzania
    'https://67.43.227.228:23737'  # Canada
]


def scrape_hot_questions():
    """Function to scrap StackExchange"""
    # Get random config.
    headers = {'User-Agent': random.choice(user_agents)}
    proxy = {'http': random.choice(proxies)}

    url = "https://stackexchange.com/"

    # Sleep between request
    time.sleep(random.uniform(1, 5))

    try:
        # Generate response
        response = get_response(url, headers, proxy, 10)

        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        question_containers = soup.find_all("div", class_="question-container")

        for container in question_containers:
            question_link = container.find("a", class_="question-link")
            if question_link:
                title = question_link.get_text(strip=True)
                link = question_link['href']
                print(f"\nTitle: {title}")
                print(f"Link: {link}")

            tags = container.find_all("a", class_="s-tag")
            tag_list = [tag.get_text(strip=True) for tag in tags]
            print("Tags:", ", ".join(tag_list))

            # Extracting meta info and structuring it
            display_additional_information(container)

    except RequestException as e:
        print(f"Error during request: {e}")


def get_response(url, headers, proxy, timeout=10):
    """
    Sends an HTTP GET request to the specified URL with the provided headers, proxy, and timeout.

    Parameters:
        url (str): The URL to request data from.
        headers (dict): The HTTP headers to use for the request.
        proxy (dict): Proxy settings for the request, which may help to evade IP-based restrictions.
        timeout (int): The maximum time in seconds to wait for a response (default is 10 seconds).

    Returns:
        response (Response): The response object if the request was successful (status code 200).
        None: If the request fails (non-200 status code).
    """
    response = requests.get(url, headers=headers, proxies=proxy, timeout=timeout)
    if response.status_code != 200:
        raise RequestException(f"Error during response: {response.status_code}")
    return response


# Todo: Reyes, need to improve regex for user_info and site_info (in progress).
def display_additional_information(container):
    """
    Extracts and displays structured metadata from a question container.

    Parameters:
        container (Tag): A BeautifulSoup Tag object representing a question container from which
                         metadata information will be extracted.

    Metadata Displayed:
        - Answers: The number of answers available for the question.
        - Asked: The relative time when the question was posted.

    Notes:
        Additional fields such as the user's name and the site can be enabled by uncommenting
        the corresponding lines in the function.
    """
    meta_data = container.find("div", class_="metaInfo")
    if meta_data:
        meta_data = meta_data.get_text(separator=" | ", strip=True)

        answers = re.search(r"(\d+)\s+answers", meta_data)
        time_info = re.search(r"asked\s+(\d+\s+\w+\s+ago)", meta_data)
        # user_info = re.search(r"by\s+(\w+)", meta_data)
        # site_info = re.search(r"on\s+(\w+)", meta_data)

        # Display structured information
        print("Aditional Info:")
        if answers:
            print(f"  Answers: {answers.group(1)}")
        if time_info:
            print(f"  Asked: {time_info.group(1)}")
        # if user_info:
            # print(f"  User: {user_info.group(1)}")
        # if site_info:
            # print(f"  Site: {site_info.group(1)}")


if __name__ == '__main__':
    scrape_hot_questions()
    # Todo: Reyes, console app (in progress).
