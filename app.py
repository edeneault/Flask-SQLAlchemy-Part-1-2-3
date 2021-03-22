"""Blogly application."""
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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
    recent_posts = Post.query.order_by(
        Post.created_at.desc()).limit(5)
    # tags = Tag.query.all()

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
    users = User.query.order_by(User.last_name, User.first_name).all()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5)
    return render_template('users/adduser.html', users=users, recent_posts=recent_posts)


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
    flash(f"USER - Name: {add_user.full_name} was added.")
    return redirect("/users")


@ app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """ Handle user edit """
    user = User.query.get_or_404(user_id)
    users = User.query.order_by(User.last_name, User.first_name).all()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5)

    return render_template('users/edit.html', user=user, users=users, recent_posts=recent_posts)


@ app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    """Handle form submission - update existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()
    flash(f"USER - Name: {user.full_name} was edited.")
    return redirect("/users")


@ app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"USER - Name: {user.full_name} was deleted.")

    return redirect("/users")


### POST ROUTES ###

@app.route('/post/allposts')
def all_posts():
    """ Show all posts """
    posts = Post.query.all()

    return render_template('/posts/allposts.html', posts=posts)


@ app.route('/users/<int:user_id>/posts/add_post')
def add_post_form(user_id):
    """ show add post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template('posts/add_post.html', user=user, tags=tags)


@ app.route('/users/<int:user_id>/posts/add_post', methods=['POST'])
def add_post_handle(user_id):
    """ handle adding a post"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    add_post = Post(title=title,
                    content=content, user=user, tags=tags)

    db.session.add(add_post)
    db.session.commit()
    flash(f"POST - Title:'{add_post.title}' was added.")

    return redirect(f"/users/{user.id}")


@ app.route('/users/<int:user_id>/posts/<int:post_id>')
def show_post(user_id, post_id):
    """show post by id"""
    post = Post.query.get_or_404(post_id)
    user = User.query.get_or_404(user_id)
    return render_template('/posts/post_show.html', post=post, user=user)


@ app.route('/users/<int:user_id>/posts/<int:post_id>/edit')
def posts_edit(user_id, post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    user = User.query.get_or_404(user_id)
    return render_template('posts/edit_post.html', post=post, user=user, tags=tags)


@ app.route('/posts/<int:post_id>/edit', methods=["POST"])
def posts_update(post_id):
    """Handle form submission for updating an existing post"""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()
    flash(f"POST - Title: '{post.title}' was edited.")

    return redirect(f"/users/{post.user_id}")


@ app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    """Handle form submission for deleting an existing post"""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"POST - Title '{post.title} deleted.")

    return redirect(f"/users/{post.user_id}")


## TAG ROUTES ##

@app.route('/tags')
def tags_alltags():
    """Show a page with info on all tags"""

    tags = Tag.query.all()
    return render_template('tags/alltags.html', tags=tags)


@app.route('/tags/addtag')
def tags_new_form():
    """Show add tag"""
    tags = Tag.query.all()
    posts = Post.query.all()
    return render_template('tags/addtag.html', posts=posts, tags=tags)


@app.route("/tags/addtag", methods=["POST"])
def tags_new():
    """Handle add tag"""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    name = Tag(name=request.form['name'], posts=posts)

    db.session.add(name)
    db.session.commit()
    flash(f"TAG - Name: '{name.name}' was added.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>')
def tags_by_id(tag_id):
    """Show tags by ID"""
    tag = Tag.query.get_or_404(tag_id)
    tags = Tag.query.all()
    posts = Post.query.all()
    return render_template('tags/showtag.html', tag=tag, tags=tags, posts=posts)


@app.route('/tags/<int:tag_id>/edit')
def tags_edit_form(tag_id):
    """Show edit form tag"""

    tags = Tag.query.all()

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template('tags/edittag.html', tag=tag, tags=tags, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):
    """Handle tag update"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']

    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"TAG - Name: '{tag.name}' was edited.")

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):
    """Handle delete tag"""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"TAG - Name: '{tag.name}' was deleted.")

    return redirect("/tags")
