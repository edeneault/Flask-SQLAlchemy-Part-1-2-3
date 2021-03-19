"""Blogly application."""
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():

    return redirect("/users")


### USER ROUTES ###

@app.route('/users')
def users_index():
    """ Show a page with info on all users """

    users = User.query.order_by(User.last_name, User.first_name).all()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5)

    return render_template('users/home.html', users=users, recent_posts=recent_posts)


@ app.route("/users/<int:user_id>")
def show_user(user_id):
    """ Show details about a single user """
    user = User.query.get_or_404(user_id)
    # post = Post.query.get_or_404(post_id)
    return render_template("users/details.html", user=user)


@ app.route('/users/adduser', methods=["GET"])
def users_new_form():
    """ Add User FORM """

    return render_template('users/adduser.html')


@ app.route("/users/adduser", methods=["POST"])
def users_new():
    """ handle adding a user """
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url']
    image_url = image_url if image_url else None

    add_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)

    db.session.add(add_user)
    db.session.commit()

    return redirect("/users")


@ app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """ Handle user edit """
    user = User.query.get_or_404(user_id)
    print(user)
    return render_template('users/edit.html', user=user)


@ app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    """Handle form submission - update existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@ app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


### POST ROUTES ###

@ app.route('/users/<int:user_id>/posts/add_post')
def add_post_form(user_id):
    user = User.query.get_or_404(user_id)
    print(user)
    return render_template('posts/add_post.html', user=user)


@ app.route('/users/<int:user_id>/posts/add_post', methods=['POST'])
def add_post_handle(user_id):
    """ handle adding a user """
    title = request.form['title']
    content = request.form['content']
    user = User.query.get_or_404(user_id)
    add_post = Post(title=title,
                    content=content, user_id=user_id)

    db.session.add(add_post)
    db.session.commit()

    return redirect(f"/users/{user.id}")


@ app.route('/users/<int:user_id>/posts/<int:post_id>')
def show_post(user_id, post_id):
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(user_id)
    return render_template('/posts/post_show.html', post=post, user=user)


@ app.route('/users/<int:user_id>/posts/<int:post_id>/edit')
def posts_edit(user_id, post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(user_id)
    return render_template('/posts/edit_post.html', post=post, user=user)


@ app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    flash(f"Post '{post.title}' edited.")

    return redirect(f"/users/{post.user_id}")


@ app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")
