"""Blogly application."""

from flask import Flask, render_template, redirect, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Users, Post, PostTag, Tag
from sqlalchemy import exc

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
    tagsRaw = request.form["tag"]
    if tagsRaw is not "":
        tags = tagsRaw.split(",")
    else:
        tags = False

    userId = user
    title = str(title) if title else None

    post = Post(title=title,content=content,user_id=userId)
    db.session.add(post)
    db.session.commit()
    
    if tags:
        for tName in tags:
            try:
                tag = Tag(name=tName)
                db.session.add(tag)
                db.session.commit()
                postTag = PostTag(tag_id=tag.id,post_id=post.id)
                db.session.add(postTag)
                db.session.commit()
            except exc.IntegrityError:
                db.session.rollback()
                tag = Tag.query.filter_by(name=tName).first()
                postTag = PostTag(tag_id=tag.id,post_id=post.id)
                db.session.add(postTag)
                db.session.commit()

    return redirect(f'/user/{userId}')


@app.route("/post/<int:post_id>")
def show_post(post_id):
    post = Post.query.get_or_404(post_id)
    postT = post.posttag
    tagL = [e.tags.name for e in postT]

    return render_template("post-detail.html", post=post, tagList=tagL)


@app.route("/delete-post/<int:post_id>")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)

    PostTag.query.filter_by(post_id=post.id).delete()
    db.session.delete(post)
    db.session.commit()

    return redirect(f'/user/{post.user_id}')


@app.route("/find-post/<tagname>")
def find_post(tagname):  
    tag = Tag.query.filter_by(name=tagname).first()
    postT = tag.posttag
    # titles = [e.posts.title for e in postT]

    return render_template("tag-posts.html", postT=postT,tag=tag)


    


