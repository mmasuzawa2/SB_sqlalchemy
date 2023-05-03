from flask_sqlalchemy import SQLAlchemy

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
                        nullable=True,
                        unique=False)
    image_url = db.Column(db.String(500), 
                          nullable=False, 
                          unique=False,
                          default="https://upload.wikimedia.org/wikipedia/commons/f/f7/Facebook_default_male_avatar.gif")