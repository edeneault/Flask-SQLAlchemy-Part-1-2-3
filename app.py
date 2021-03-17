"""Blogly application."""
from flask import Flask, request, render_template,  redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

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


@app.route('/users')
def users_index():
    """ Show a page with info on all users """

    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/home.html', users=users)


@app.route("/users/<int:user_id>")
def show_pet(user_id):
    """ Show details about a single user """
    user = User.query.get_or_404(user_id)
    return render_template("users/details.html", user=user)


@app.route('/users/adduser', methods=["GET"])
def users_new_form():
    """ Add User FORM """

    return render_template('users/adduser.html')


@app.route("/users/adduser", methods=["POST"])
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


@app.route('/users/<int:user_id>/edit')
def users_edit(user_id):
    """ Handle user edit """
    user = User.query.get_or_404(user_id)
    print(user)
    return render_template('users/edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def users_update(user_id):
    """Handle form submission - update existing user"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def users_destroy(user_id):
    """Handle form submission for deleting an existing user"""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
