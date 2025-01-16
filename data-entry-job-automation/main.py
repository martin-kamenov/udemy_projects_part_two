from typing import Tuple, List
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
import requests
import time
import os

load_dotenv()

FORM_LINK = os.getenv("FORM_END")
WEBSITE = "https://appbrewery.github.io/Zillow-Clone/"

def get_properties_data() -> Tuple[List, List, List]:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
        "Accept-Language": "en-US,en;q=0.9",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate"
    }
    response = requests.get(WEBSITE, headers=headers)
    response.raise_for_status()
    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")
    all_link_elements = soup.select(".StyledPropertyCardPhotoWrapper a")
    all_links = [link["href"] for link in all_link_elements]

    all_price_elements = soup.select(".PropertyCardWrapper span")
    all_prices = [price.getText()[:6] for price in all_price_elements]

    all_address_elements = soup.select(".StyledPropertyCardDataWrapper address")
    all_addresses = [address_.getText().strip() for address_ in all_address_elements]
    all_addresses = [address_.replace(" | ", " ") for address_ in all_addresses]

    return all_links, all_prices, all_addresses


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get(FORM_LINK)

links, prices, addresses = get_properties_data()

for index in range(len(links)):
    time.sleep(2)
    address = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
    price_per_month = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
    property_link = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')

    time.sleep(3)
    address.send_keys(addresses[index])
    time.sleep(1)
    price_per_month.send_keys(prices[index])
    time.sleep(1)
    property_link.send_keys(links[index], Keys.END)

    send_button = driver.find_element(By.XPATH, value='//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
    send_button.click()

    time.sleep(2)
    another_answer = driver.find_element(By.CSS_SELECTOR, value='div a')
    another_answer.click()
