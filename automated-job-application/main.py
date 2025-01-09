# 90%
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import dotenv
import time
import os

dotenv.load_dotenv()

ACCOUNT_EMAIL = os.getenv("EMAIL")
ACCOUNT_PASSWORD = os.getenv("PASSWORD")
should_call_link = False


def log_in():
    time.sleep(2)
    try:
        global should_call_link
        should_call_link = True
        time.sleep(3)
        reject_button = driver.find_element(By.CSS_SELECTOR, value='button[action-type="DENY"]')
        reject_button.click()

        time.sleep(2)
        sign_in_button = driver.find_element(By.LINK_TEXT, value='Sign in')
        sign_in_button.click()

        time.sleep(3)
        email_input = driver.find_element(By.ID, value="username")
        password_input = driver.find_element(By.ID, value="password")
    except NoSuchElementException:
        try:
            driver.find_element(By.CSS_SELECTOR, value='button[data-modal="base-sign-in-modal"]').click()

            time.sleep(5)
            email_input = driver.find_element(By.ID, value="base-sign-in-modal_session_key")
            password_input = driver.find_element(By.ID, value="base-sign-in-modal_session_password")

        except NoSuchElementException:
            time.sleep(3)
            reject_button = driver.find_element(By.CSS_SELECTOR, value='button[action-type="DENY"]')
            reject_button.click()

            time.sleep(3)
            email_input = driver.find_element(By.ID, value="username")
            password_input = driver.find_element(By.ID, value="password")

        email_input.send_keys(ACCOUNT_EMAIL)
        password_input.send_keys(ACCOUNT_PASSWORD)
        password_input.send_keys(Keys.ENTER)

    email_input.send_keys(ACCOUNT_EMAIL)
    password_input.send_keys(ACCOUNT_PASSWORD)
    password_input.send_keys(Keys.ENTER)


def apply():
    time.sleep(3)
    driver.find_element(By.CSS_SELECTOR, value=".jobs-s-apply button").click()

    time.sleep(2)
    phone = driver.find_element(By.CSS_SELECTOR, value="input[id*=phoneNumber]")
    if phone.text == "":
        phone.send_keys("0123456789")

    submit_button = driver.find_element(By.CSS_SELECTOR, value="footer button")
    if submit_button.get_attribute("data-control-name") == "continue_unify":
        abort_application()
        print("Complex application, skipped.")
        return
    else:
        print("Submitting job application.")
        submit_button.click()


def abort_application():
    close_button = driver.find_element(By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_button.click()

    time.sleep(2)
    discard_button = driver.find_elements(By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[1]
    discard_button.click()


def call_link():
    time.sleep(2)
    driver.get(
        "https://www.linkedin.com/jobs/search/?currentJobId=4081810683"
        "&f_AL=true&geoId=105333783&keywords=happy"
        "&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true&sortBy=R"
    )


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
call_link()

log_in()

if should_call_link:
    call_link()

all_jobs = driver.find_elements(By.CSS_SELECTOR, value=".job-card-container--clickable")

for job in all_jobs:
    print("Opening listing")
    job.click()

    try:
        apply()
    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()