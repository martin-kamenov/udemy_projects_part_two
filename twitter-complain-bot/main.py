from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from dotenv import load_dotenv
import time
import os


load_dotenv()

PROMISED_UP = 50
PROMISED_DOWN = 100
TWITTER_EMAIL = os.getenv("EMAIL")
TWITTER_PASSWORD = os.getenv("PASSWORD")
TWITTER_USERNAME = os.getenv("USER_NAME")
SPEEDTEST_WEBSITE = "https://www.speedtest.net/"
TWITTER_WEBSITE = "https://www.x.com"


class InternetSpeedTwitterBot:

    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_experimental_option("detach", True)
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.up = 0
        self.down = 0

    def get_internet_speed(self):
        self.driver.get(SPEEDTEST_WEBSITE)

        time.sleep(2)
        reject_button = self.driver.find_element(By.ID, value="onetrust-reject-all-handler")
        reject_button.click()

        go_button = self.driver.find_element(By.CLASS_NAME, value="start-button")
        go_button.click()

        time.sleep(60)
        download = self.driver.find_element(
            By.XPATH,
            value='//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/'
                  'div[3]/div/div[3]/div/div/div[2]/div[1]/div[1]/div/div[2]/span'
        )
        upload = self.driver.find_element(
            By.XPATH,
            value='//*[@id="container"]/div[1]/div[3]/div/div/div/div[2]/div[3]/'
                  'div[3]/div/div[3]/div/div/div[2]/div[1]/div[2]/div/div[2]/span'
        )

        self.down = download.text
        self.up = upload.text

        print(f"down: {self.down}")
        print(f"up: {self.up}")

    def tweet_at_provider(self):
        self.driver.get(TWITTER_WEBSITE)

        time.sleep(2)
        reject_button = self.driver.find_element(
            By.XPATH,
            value='//*[@id="layers"]/div/div[1]/div/div/div/div[2]/button[2]/div'
        )
        reject_button.click()

        time.sleep(1)
        close_button = self.driver.find_element(
            By.XPATH,
            value='//*[@id="layers"]/div/div[2]/div/div/div/button'
        )
        close_button.click()

        time.sleep(1)
        sign_in = self.driver.find_element(
            By.XPATH,
            value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div[1]/div[1]/div/div[3]/div[3]/a/div/span'
        )
        sign_in.click()

        time.sleep(3)
        input_email = self.driver.find_element(
            By.CSS_SELECTOR,
            value='div input'
        )
        input_email.send_keys(TWITTER_EMAIL, Keys.ENTER)

        try:
            time.sleep(2)
            username = self.driver.find_element(
                By.CSS_SELECTOR,
                value='div input'
            )
            username.send_keys(TWITTER_USERNAME, Keys.ENTER)
        except NoSuchElementException:
            ...

        time.sleep(3)
        password_input = self.driver.find_element(
            By.XPATH,
            value='//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div/'
                  'div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input'
        )
        password_input.send_keys(TWITTER_PASSWORD, Keys.ENTER)

        time.sleep(3)
        if float(PROMISED_DOWN) > float(self.down):
            twit_input = self.driver.find_element(
                By.XPATH,
                value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/'
                      'div/div[3]/div/div[2]/div[1]/div/div/div/div[2]/div[1]/div/'
                      'div/div/div/div/div/div/div/div/div/div/div[1]/div/div/div/'
                      'div/div/div[2]/div/div/div/div'
            )
            twit_input.click()
            twit_input.send_keys(f"Hey Internet Provider, why is my internet speed {self.down}down/{self.up}up "
                                 f"when i pay for 150down/50up?")

            post_twit_button = self.driver.find_element(
                By.XPATH,
                value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[3]/div/div[2]/'
                      'div[1]/div/div/div/div[2]/div[2]/div[2]/div/div/div/button/div/span/span'
            )
            post_twit_button.click()

            time.sleep(2)
            self.driver.quit()

            # time.sleep(2)
            # x_button = self.driver.find_element(
            #     By.CSS_SELECTOR,
            #     value='button div svg'
            # )
            # x_button.click()


bot = InternetSpeedTwitterBot()
bot.get_internet_speed()
bot.tweet_at_provider()
