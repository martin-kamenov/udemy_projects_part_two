from bs4 import BeautifulSoup
import requests
import smtplib
import os

END_POINT = "https://www.amazon.com/dp/B075CYMYK6?psc=1&ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6"
EMAIl = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("MY_PASSWORD")
BUY_PRICE = 100
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate"
}


def get_product_price_and_name():
    response = requests.get(url=END_POINT, headers=headers)
    response.raise_for_status()
    website_html = response.text

    soup = BeautifulSoup(website_html, "html.parser")
    found_price = soup.find(class_="aok-offscreen")
    price = float(found_price.getText().strip()[1:])

    product = soup.find(id="productTitle").getText()
    lines = product.splitlines()
    stripped_lines = [line.strip() for line in lines]
    product_name_ = " ".join(stripped_lines)

    print(soup.prettify())

    return price, product_name_


product_price, product_name = get_product_price_and_name()
message = f"{product_name} is now ${product_price}"


def send_email():
    with smtplib.SMTP_SSL("smtp.gmail.com") as connection:
        connection.login(user=EMAIl, password=PASSWORD)
        connection.sendmail(
            from_addr=EMAIl,
            to_addrs="mar7onzi@gmail.com",
            msg=f"Subject: Amazon Price Alert \n\n{message}\n{END_POINT}".encode("utf-8")
        )
        print("Message sent.")


if product_price < BUY_PRICE:
    send_email()
    print(product_price)
    print(product_name)