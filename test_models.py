from unittest import TestCase

from app import app
from models import db, User

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

    def full_name(self):
        user = User(first_name="firstName", last_name="lastName",
                    image_url="https://a.wattpad.com/useravatar/ScuffedMisfit.256.87195.jpg")
        self.assertEqual(user.full_name(), "firstName lastName")
