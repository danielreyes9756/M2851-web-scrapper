import time
import random
import pandas as pd
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from src.logic.data_extractor import extract_question_data
from src.logic.driver_setup import try_setup_with_proxy


def scrape_hot_questions():
    url = "https://stackexchange.com/"
    driver = try_setup_with_proxy(url)

    questions_data = []
    try:
        while True:
            # Wait for body
            WebDriverWait(driver, 10).until(
                ec.presence_of_element_located((By.TAG_NAME, "body"))
            )
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            question_containers = soup.find_all("div", class_="question-container")
            for container in question_containers:
                question_data = extract_question_data(container)
                questions_data.append(question_data)
            try:
                next_button = driver.find_elements(By.XPATH, "//a[@rel='next']//span[@class='page-numbers next']")
                if not next_button:
                    print("Not Found button 'next' -- ¡¡ Finish !!")
                    break
                if next_button[0].is_displayed() and next_button[0].is_enabled():
                    driver.execute_script("arguments[0].scrollIntoView(true);", next_button[0])
                    next_button[0].click()
                    time.sleep(random.uniform(1, 3))
                else:
                    print("No more pages or 'next' button is not interactable.")
                    break
            except Exception as e:
                print(f"Exception while trying to get next button: {e}")
                break
    finally:
        driver.quit()

    if questions_data:
        df = pd.DataFrame(questions_data)
        df.to_csv('questions.csv', index=False)
        print("Data saved to questions.csv")
