from unittest import TestCase

from datetime import datetime as dt
import datetime
from app import app
from models import db, User, Post, Tag

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test_db'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()


class UserModelTestCase(TestCase):
    """Tests for model for users."""

    def setUp(self):
        """Clean up any existing users."""

        User.query.delete()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_full_name(self):
        """ User Class Method test """
        user = User(first_name="firstName", last_name="lastName")
        self.assertEqual(user.full_name, "firstName lastName")

    def test_friendly_date(self):
        """ Post Class Method Test """
        post = Post(title="firstPost", content="content",
                    created_at=datetime.datetime(2021, 3, 19, 6, 4, 6, 802286), user_id=1)
        self.assertEqual(post.friendly_date,
                         "Fri Mar 19  2021, 6:04 AM")
        # self.assertEqual(post.friendly_date(), "2021-03-19 06:04:06.802286")
