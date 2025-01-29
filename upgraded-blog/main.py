from flask import Flask, render_template, request
from datetime import datetime
from dotenv import load_dotenv
import os
import requests
import smtplib

load_dotenv()

EMAIL = os.getenv("EMAIl")
PASSWORD = os.getenv("PASS")

app = Flask(__name__)
now = datetime.now().date()


def get_blog_data():
    all_blogs = requests.get(url="https://api.npoint.io/674f5423f73deab1e9a7").json()
    return all_blogs


def send_email(name, email, phone, message):
    try:
        message = f"Subject:New Message\n\n" \
                  f"Name: {name}\n" \
                  f"Email: {email}\n" \
                  f"Phone number: {phone}\n" \
                  f"Message: {message}"

        with smtplib.SMTP_SSL("smtp.gmail.com", port=465) as connection:
            connection.login(
                user=EMAIL,
                password=PASSWORD,
            )
            connection.sendmail(
                from_addr=EMAIL,
                to_addrs=EMAIL,
                msg=message
            )
            print("Message sent.")
    except smtplib.SMTPAuthenticationError as error:
        print(f"Authentication failed: {error}")
    except Exception as e:
        print(f"Failed to send email: {e}")


@app.route("/")
def home():
    data = get_blog_data()
    return render_template("index.html", all_posts=data, date=now)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        send_email(data['name'], data['email'], data['phone'], data['message'])
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)


@app.route('/post/<int:index>')
def show_post(index):
    all_posts = get_blog_data()
    requested_post = None

    for post in all_posts:
        if post.get('id') == index:
            requested_post = post

    return render_template("post.html", post=requested_post, date=now)


if __name__ == "__main__":
    app.run(debug=True)