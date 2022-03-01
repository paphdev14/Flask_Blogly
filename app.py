"""Blogly application."""

from crypt import methods
from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SECRET_KEY'] = "oh-so-secret"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()


@app.route('/')
def home():
    """Redirect to list of users"""
    return redirect('/users')

# ===================== User Routes ===================== #


@app.route('/users')
def homepage():
    """Show list of fullname on the homepage"""
    users = User.query.all()
    return render_template('users/userList.html', users=users)


@app.route('/users/new')
def user_form():
    """Show create user form"""
    return render_template('users/userForm.html')


@app.route('/users/new', methods=['POST'])
def new_user():
    """Create new user"""
    """Add them to DB"""
    new_user = User(
        first_name=request.form['first_name'],
        last_name=request.form['last_name'],
        image_url=request.form['image_url'] or None
    )
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>')
def users_list(user_id):
    """Show info user by their id"""
    user = User.query.get_or_404(user_id)
    return render_template('users/userPage.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_form(user_id):
    """To show editing user form"""
    user = User.query.get_or_404(user_id)
    user = User.query.get_or_404(user_id)
    return render_template('users/userEdit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Edit existing user"""
    """Update them to DB"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete existing user"""
    """Delete them to DB"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


# ===================== Post Routes ===================== #
@app.route('/users/<int:user_id>/posts/new')
def new_posts_form(user_id):
    """Show user post form"""
    user = User.query.get_or_404(user_id)
    return render_template("/posts/newPosts.html", user=user)
