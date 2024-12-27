from selenium import webdriver
from selenium.webdriver.common.by import By

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

drive = webdriver.Chrome(options=chrome_options)
drive.get("https://www.python.org")

event_dates = drive.find_elements(By.CSS_SELECTOR, value=".event-widget li time")
event_titles = drive.find_elements(By.CSS_SELECTOR, value=".event-widget li a")

upcoming_events = {}

for index in range(len(event_titles)):
    upcoming_events[index] = {"time": event_dates[index].text, "name": event_titles[index].text}

print(upcoming_events)

drive.quit()