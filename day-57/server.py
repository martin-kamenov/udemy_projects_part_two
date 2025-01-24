from flask import Flask, render_template
from random import randint
from datetime import datetime
import requests

app = Flask(__name__)


@app.route("/")
def home():
    random_number = randint(1, 10)
    year = datetime.now().year
    creator_name = "Martin"
    return render_template(
        "index.html",
        num=random_number,
        current_year=year,
        name=creator_name
    )


@app.route("/blog/<num>")
def get_blog(num):
    print(num)
    blog_url = "https://api.npoint.io/87962172a86f2671f9da"
    response = requests.get(url=blog_url)
    all_posts = response.json()
    return render_template("blog.html", posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)