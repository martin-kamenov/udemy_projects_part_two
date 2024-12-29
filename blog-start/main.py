from flask import Flask, render_template
from post import Post
import requests

app = Flask(__name__)

def get_posts_data():
    posts = requests.get(url="https://api.npoint.io/c790b4d5cab58020d391").json()
    all_posts = [Post(post["id"], post["body"], post["title"], post["subtitle"]) for post in posts]
    return all_posts


@app.route('/')
def home():
    all_posts = get_posts_data()
    return render_template("index.html", all_posts=all_posts)


@app.route('/post/<int:index>')
def show_post(index):
    all_posts = get_posts_data()
    requested_post = None

    for post in all_posts:
        if post.id == index:
            requested_post = post

    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True)

get_posts_data()