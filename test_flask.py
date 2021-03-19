from unittest import TestCase

from datetime import datetime as dt
import datetime

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for users."""

    def setUp(self):
        """Add sample user."""
        Post.query.delete()
        User.query.delete()

        user = User(first_name="firstName", last_name="lastName",
                    image_url="https://a.wattpad.com/useravatar/ScuffedMisfit.256.87195.jpg")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('firstName', html)

    def test_details_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<p class="card-text">First Name: firstName</p>', html)
            self.assertIn(self.user.image_url, html)

    def test_add_user(self):
        with app.test_client() as client:
            d = {"first_name": "nameSecond", "last_name": "lastSecond",
                 "image_url": "https://a.wattpad.com/useravatar/ScuffedMisfit.256.87195.jpg"}
            resp = client.post("/users/adduser", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('nameSecond lastSecond</a></td>', html)


class PostViewsTestCase(TestCase):
    """Tests for views for posts."""

    def setUp(self):
        """Add sample user and post."""
        print("INSIDE SET UP CLASS")
        Post.query.delete()
        User.query.delete()

        user = User(first_name="nameSecond", last_name="lastSecond",
                    image_url="https://a.wattpad.com/useravatar/ScuffedMisfit.256.87195.jpg")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.user = user

        post = Post(title="firstPost", content="content",
                    user_id=1)
        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.post = post

    def tearDown(self):
        """Clean up any fouled transaction."""
        print("INSIDE TEAR DOWN CLASS")
        db.session.remove()
        db.drop_all()
        db.create_all()
        db.session.rollback()

    def test_posts(self):
        """ test if post show appear in homepage """
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('firstPost', html)

    def test_show_post(self):
        """  test if post content is present in show_post view """
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('firstPost', html)

    def test_add_post(self):
        """  test if post can successfully be added """
        with app.test_client() as client:
            d = {"title": "titleTest", "content": "contentTest",
                 "user_id": 1}
            resp = client.post(
                f"/users/{self.user_id}/posts/add_post", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '>titleTest</a>', html)
