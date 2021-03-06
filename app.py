"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    tags = Tag.query.all()
    return render_template("/posts/newPosts.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_posts(user_id):
    """Submit and create new user posts"""
    user = User.query.get_or_404(user_id)

    """Copied & pasted that piece of code below, but don't really get it in full"""
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    """Copied & pasted that piece of code above, but don't really get it in full"""

    new_post = Post(title=request.form['title'],
                    content=request.form['content'], user=user, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_posts(post_id):
    """Show user post info"""
    post = Post.query.get_or_404(post_id)
    return render_template('/posts/showPost.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def post_form(post_id):
    """Show edit post form"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('/posts/editPost.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Updating existing user posts"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def del_post(post_id):
    """Deleting existing user posts"""
    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


# ===================== Tags Routes ===================== #
@app.route('/tags')
def tags_index():
    """Page info all tags"""

    tags = Tag.query.all()
    return render_template('tags/index.html', tags=tags)


@app.route('/tags/new')
def tags_form():
    """Form to create a new tag"""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route("/tags/new", methods=["POST"])
def tags_new():
    """Form submission for creating a new tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form['name'], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_show(tag_id):
    """Show a page with info on a specific tag"""

    tag = Tag.query.get_or_404(tag_id)
    return render_template('tags/showTags.html', tag=tag)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Form submission for deleting existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
