from selenium import webdriver
from selenium.webdriver.common.by import By
import time


def check_prices():
    money_string = driver.find_element(By.ID, value="money").text
    if "," in money_string:
        money_string = money_string.replace(",", "")
    money = int(money_string)

    all_prices = driver.find_elements(By.CSS_SELECTOR, value="#store b")
    prices = []

    for price in all_prices:
        price_element = price.text

        if price_element != "":
            cost = int(price_element.split("-")[1].strip().replace(",", ""))
            prices.append(cost)

    cookie_upgrades = {}
    for index in range(len(prices)):
        cookie_upgrades[prices[index]] = item_ids[index]

    possible_upgrades = {}
    for cost, id_ in cookie_upgrades.items():
        if money > cost:
            possible_upgrades[cost] = id_

    if max(possible_upgrades):
        highest_affordable_upgrade = max(possible_upgrades)
        print(highest_affordable_upgrade)
        id_to_purchase = possible_upgrades[highest_affordable_upgrade]

        driver.find_element(By.ID, value=id_to_purchase).click()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
driver.get("https://orteil.dashnet.org/experiments/cookie/")

cookie = driver.find_element(By.ID, value="cookie")

items = driver.find_elements(By.CSS_SELECTOR, value="#store div")
item_ids = [el.get_attribute("id") for el in items]

five_min = time.time() + 6*50
time_out = time.time()  + 5

while True:
    cookie.click()

    if time.time() > time_out:
        check_prices()
        time_out = time.time() + 5

    if time.time() > five_min:
        cookie_per_sec = driver.find_element(By.ID, value="cps").text
        print(cookie_per_sec)
        break