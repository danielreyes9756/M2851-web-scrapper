import re


def __extract_question_link(container):
    """Extracts the question link."""
    question_link = container.find("a", class_="question-link")
    return question_link['href'] if question_link else "N/A"


def __extract_question_title(container):
    """Extracts the question title."""
    question_link = container.find("a", class_="question-link")
    return question_link.get_text(strip=True) if question_link else "N/A"


def __extract_tags(container):
    """Extracts tags associated with the question."""
    tags = container.find_all("a", class_="s-tag")
    return [tag.get_text(strip=True) for tag in tags]


def __extract_answers_count(meta_data_text):
    """Extracts the number of answers."""
    answers_match = re.search(r"(\d+)\s+answers", meta_data_text)
    return answers_match.group(1) if answers_match else "N/A"


def __extract_time_asked(meta_data_text):
    """Extracts the time the question was asked."""
    time_match = re.search(r"asked\s+(.+?)(?:\s+by|$)", meta_data_text)
    return time_match.group(1).rstrip('|').strip() if time_match else "N/A"


def __extract_author_and_link(meta_data):
    """Extracts the author name and link."""
    author_tag = meta_data.find("span", class_="owner")
    if author_tag:
        author_link_tag = author_tag.find("a")
        author = author_link_tag.get_text(strip=True) if author_link_tag else "N/A"
        author_link = author_link_tag['href'] if author_link_tag else "N/A"
        return author, author_link
    return "N/A", "N/A"


def __extract_question_host(meta_data):
    """Extracts the host of the question."""
    host_tag = meta_data.find("a", class_="question-host")
    return host_tag.get_text(strip=True) if host_tag else "N/A"


def __extract_meta_data(container):
    """Extracts meta information such as answers, asked time, author, and host."""
    meta_data = container.find("div", class_="metaInfo")
    if meta_data:
        meta_data_text = meta_data.get_text(separator=" | ", strip=True)
        answers_count = __extract_answers_count(meta_data_text)
        time_asked = __extract_time_asked(meta_data_text)
        author, author_link = __extract_author_and_link(meta_data)
        question_host = __extract_question_host(meta_data)

        return answers_count, time_asked, author, author_link, question_host
    return "N/A", "N/A", "N/A", "N/A", "N/A"


def extract_question_data(container):
    """Combines all data extraction."""
    title = __extract_question_title(container)
    link = __extract_question_link(container)
    tags = __extract_tags(container)
    answers, time_asked, author, author_link, question_host = __extract_meta_data(container)

    return {
        'title': title,
        'link': link,
        'tags': ", ".join(tags),
        'answers': answers,
        'asked_time': time_asked,
        'author': author,
        'author_link': author_link,
        'question_host': question_host
    }
