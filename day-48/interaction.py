from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Keep browser open after program finishes
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

# Create and configure the Chrome webdriver
drive = webdriver.Chrome(options=chrome_options)

# Navigate to Wikipedia
drive.get("https://en.wikipedia.org/wiki/Main_Page")

article_count = drive.find_element(By.CSS_SELECTOR, value="#articlecount a")
# article_count.click()

# Find element by Link Text
all_portals = drive.find_element(By.LINK_TEXT, value="Content portals")
# all_portals.click()

# Find the "Search" input by Name
search = drive.find_element(By.NAME, value="search")

# Sending keyboard input to Selenium
search.send_keys("Python")

# drive.quit()