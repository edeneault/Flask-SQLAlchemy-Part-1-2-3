"""Seed file to make sample data for users and posts db."""

from models import User, Post, db
from app import app
import datetime

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()
Post.query.delete()

# set date variable for input

curr_date = datetime.today().strftime('%Y-%m-%d')
print(curr_date)

# Add users
etienne = User(first_name="Etienne", last_name="Deneault",
               image_url="https://via.placeholder.com/150.png/FFFF00/00000?text=USER_IMG")
leonard = User(first_name="Leonard", last_name="Deneault",
               image_url="https://via.placeholder.com/150.png/FFFF00/00000?text=USER_IMG")
alexandra = User(first_name="Alexandra", last_name="Deneault",
                 image_url="https://via.placeholder.com/150.png/FFFF00/00000?text=USER_IMG")

# # Add posts

post_1_1 = Post(title="First Post", content="This is my first post",
                user_id=1)
post_1_2 = Post(title="Second Post", content="This is my second post",
                user_id=1)
post_1_3 = Post(title="Third Post", content="This is my third post",
                user_id=1)
post_1_4 = Post(title="Fourth Post", content="This is my fourth post",
                user_id=1)
post_1_5 = Post(title="Fifth Post", content="This is my fifth post",
                user_id=1)

post_2_1 = Post(title="First Post", content="This is my first post",
                user_id=2)
post_2_2 = Post(title="Second Post", content="This is my second post",
                user_id=2)
post_2_3 = Post(title="Third Post", content="This is my third post",
                user_id=2)
post_2_4 = Post(title="Fourth Post", content="This is my fourth post",
                user_id=2)
post_2_5 = Post(title="Fifth Post", content="This is my fifth post",
                user_id=2)

post_3_1 = Post(title="First Post", content="This is my first post",
                user_id=3)
post_3_2 = Post(title="Second Post", content="This is my second post",
                user_id=3)
post_3_3 = Post(title="Third Post", content="This is my third post",
                user_id=3)
post_3_4 = Post(title="Fourth Post", content="This is my fourth post",
                user_id=3)
post_3_5 = Post(title="Fifth Post", content="This is my fifth post",
                user_id=3)

posts = [post_1_1, post_1_2, post_1_3, post_1_4, post_1_5, post_2_1, post_2_2, post_2_3, post_2_4, post_2_5,
         post_3_1, post_3_2, post_3_3, post_3_4, post_3_5]

# Add new objects to session, so they'll persist
db.session.add(etienne)
db.session.add(leonard)
db.session.add(alexandra)
db.session.add_all(posts)

# Commit--otherwise, this never gets saved!
db.session.commit()
