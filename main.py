import datetime

from flask import Flask, render_template
import os
import requests
from post import Post

AUTHOR = "Cristina"
npoint_endpoint = os.environ.get("NPOINT_ENDPOINT")
npoint_data = requests.get(url=npoint_endpoint).json()


posts = [
    Post(id=post_data["id"],
         title=post_data["title"],
         subtitle=post_data["subtitle"],
         body=post_data["body"],
         image_url=post_data["image_url"],
         author=AUTHOR
         )
    for post_data in npoint_data
]

current_year = datetime.datetime.now().year

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def home():
    return render_template("index.html", posts=posts, author=AUTHOR, year=current_year)


@app.route("/about")
def about():
    return render_template("about.html", year=current_year)


@app.route("/contact")
def contact():
    return render_template("contact.html", year=current_year)


@app.route("/post/<index>")
def post(index):
    for post_data in posts:
        if post_data.id == int(index):
            target_post = post_data
    return render_template("post.html", post=target_post, year=current_year)


if __name__ == "__main__":
    app.run(debug=True)
