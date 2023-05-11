"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "mokomichi1"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

with app.app_context():
    connect_db(app)
    # db.drop_all()
    # db.create_all()


@app.route("/")
def list_users():
    users = Users.query.all()
    return render_template("user-list.html", users=users)


@app.route("/show-form")
def show_form():
    return render_template("add-user-form.html")


@app.route("/", methods=["POST"])
def add_user():
    firstName = request.form['firstName']
    lastName = request.form['lastName']
    image = request.form['image']
    image = str(image) if image else None

    user = Users(first_name=firstName, last_name=lastName, image_url=image)

    with app.app_context():
        db.session.add(user)
        db.session.commit()

    return redirect("/")
    # return redirect(f"/{pet.id}")


@app.route("/update-user/<int:user_id>")
def show_update_form(user_id):
    id = user_id
    return render_template("update-form.html", id = id)


@app.route("/update/<int:user_id>", methods=["POST"])
def update_user(user_id):
    user = Users.query.get_or_404(user_id)

    firstName = request.form['firstName']
    lastName = request.form['lastName']
    image = request.form['image']

    if firstName:
        user.first_name = firstName
    if lastName:
        user.last_name = lastName
    if image:
        user.image_url = image

    db.session.add(user)
    db.session.commit()

    return redirect("/")


@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template("user_detail.html", user=user)


@app.route("/delete/<int:user_id>")
def delete_user(user_id):
    user = Users.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/")


@app.route("/show-post-form/<int:user_id>")
def show_post_form(user_id):
    user = Users.query.get_or_404(user_id)
    return render_template("posting-form.html", user=user)


@app.route("/post-form/<int:user>", methods=["POST"])
def handle_post(user):
    title = request.form["title"]
    content = request.form["content"]
    userId = user
    title = str(title) if title else None

    post = Post(title=title,content=content,user_id=userId)

    db.session.add(post)
    db.session.commit()

    return redirect(f'/user/{userId}')


@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post-detail.html", post=post)


@app.route("/delete-post/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f'/user/{post.user_id}')