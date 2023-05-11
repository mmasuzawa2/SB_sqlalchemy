from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False,
                     unique=False)
    last_name = db.Column(db.String(50), 
                        nullable=False,
                        unique=False)
    image_url = db.Column(db.String(500), 
                          nullable=False, 
                          unique=False,
                          default="https://upload.wikimedia.org/wikipedia/commons/f/f7/Facebook_default_male_avatar.gif")
    


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(200),
                     nullable=False,
                     default = "no title")
    content = db.Column(db.Text,
                     nullable=False)
    created_at = db.Column(db.DateTime(timezone=True),
                           nullable = False,
                           default = datetime.datetime.utcnow)
    user_id = db.Column(db.Integer, 
                        db.ForeignKey("users.id"))
    
    users = db.relationship('Users', backref='posts')
    