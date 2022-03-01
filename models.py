"""Models for Blogly."""

import datetime
from email.policy import default
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMG_URL = "https://static.thenounproject.com/png/1081856-200.png"


def connect_db(app):
    db.app = app
    db.init_app(app)


# Model code goes here
class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                           nullable=False,
                           unique=True)
    last_name = db.Column(db.String(50),
                          nullable=False,
                          unique=True)
    image_url = db.Column(db.Text,
                          nullable=False,
                          unique=False, default=DEFAULT_IMG_URL)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Text,
                   primary_key=True)
    title = db.Column(db.Text,
                      nullable=False,
                      unique=True)
    content = db.Column(db.Text,
                        nullable=False,
                        unique=True)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'), nullable=False)

    @property
    def friendly_date(self):
        """Friendly formatted date."""
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")
