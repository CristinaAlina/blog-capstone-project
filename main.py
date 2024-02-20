from flask import Flask, render_template, request
import os
import requests
import datetime
from post import Post
import smtplib

AUTHOR = "Cristina"

my_email = os.environ.get("MY_EMAIL")
email_password = os.environ.get("EMAIL_PASS")

npoint_endpoint = os.environ.get("NPOINT_ENDPOINT")  # Use your own npoint link
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


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form

        # Send email to yourself with received form data
        send_email(data)

        return render_template("contact.html", year=current_year, form_submitted=True)
    else:
        return render_template("contact.html", year=current_year, form_submitted=False)


@app.route("/post/<index>")
def post(index):
    for post_data in posts:
        if post_data.id == int(index):
            target_post = post_data
    return render_template("post.html", post=target_post, year=current_year)


def send_email(form_data):
    name = form_data["name"]
    email = form_data["email"]
    phone = form_data["phone"]
    message = form_data["message"]
    with smtplib.SMTP("smtp.gmail.com", port=587, timeout=120) as connection:
        connection.starttls()
        connection.login(user=my_email, password=email_password)

        msg_body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"

        connection.sendmail(from_addr=email,
                            to_addrs=my_email,
                            msg=f"Subject: New Message\n\n{msg_body}")


if __name__ == "__main__":
    app.run()
