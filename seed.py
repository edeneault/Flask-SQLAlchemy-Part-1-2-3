"""Seed file to make sample data for users and posts db."""

from models import User, Post, Tag, PostTag, db
from app import app
from datetime import datetime as dt
import datetime

## CREATE ALL TABLES ##
db.drop_all()
db.create_all()

## IF TABLE NOT EMPTY => EMPTY ##
User.query.delete()
Post.query.delete()
Tag.query.delete()

# SET DATE ##

curr_date = datetime.datetime.now().strftime('%Y-%m-%d')
print(curr_date)

## ADD USERS ##
etienne = User(first_name="Etienne", last_name="Deneault",
               image_url="https://miro.medium.com/max/3150/1*vx4SBuW5YM3s1Pxyk00mSQ.jpeg")
taylor = User(first_name="Taylor", last_name="Deneault",
              image_url="https://trupanion.com/blog/wp-content/uploads/2017/02/cat-1646566_640.jpg")
alexandra = User(first_name="Alexandra", last_name="Deneault",
                 image_url="https://iv1.lisimg.com/image/20508627/666full-alexandra-apjarova.jpg")

## ADD POSTS ##

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


## ADD TAGS ##

tag_1 = Tag(name="info")
tag_2 = Tag(name="story")
tag_3 = Tag(name="editorial")
tag_4 = Tag(name="animals")
tag_5 = Tag(name="family")

tags = [tag_1, tag_2, tag_3, tag_4, tag_5]

## ADD POSTS-TAGS ##

post_tag_1 = PostTag(post_id=1, tag_id=1)
post_tag_2 = PostTag(post_id=1, tag_id=2)
post_tag_3 = PostTag(post_id=1, tag_id=3)
post_tag_4 = PostTag(post_id=2, tag_id=2)
post_tag_5 = PostTag(post_id=2, tag_id=3)
post_tag_6 = PostTag(post_id=5, tag_id=4)
post_tag_7 = PostTag(post_id=3, tag_id=3)
post_tag_8 = PostTag(post_id=4, tag_id=4)
post_tag_9 = PostTag(post_id=6, tag_id=5)
post_tag_10 = PostTag(post_id=7, tag_id=1)
post_tag_11 = PostTag(post_id=8, tag_id=2)
post_tag_12 = PostTag(post_id=9, tag_id=3)
post_tag_13 = PostTag(post_id=10, tag_id=5)
post_tag_14 = PostTag(post_id=11, tag_id=1)
post_tag_15 = PostTag(post_id=12, tag_id=4)
post_tag_16 = PostTag(post_id=13, tag_id=3)
post_tag_17 = PostTag(post_id=14, tag_id=4)
post_tag_18 = PostTag(post_id=15, tag_id=5)

posts_tags = [post_tag_1, post_tag_2, post_tag_3, post_tag_4, post_tag_5, post_tag_6,
              post_tag_7, post_tag_8, post_tag_9, post_tag_10, post_tag_11, post_tag_12,
              post_tag_13, post_tag_14, post_tag_15, post_tag_16, post_tag_17, post_tag_18]

## ADD OBJECTS TO SESSION ##
db.session.add(etienne)
db.session.add(taylor)
db.session.add(alexandra)
db.session.add_all(posts)
db.session.add_all(tags)


## COMMIT !IMPORTANT ##
db.session.commit()


## COMMIT AFTER CREATION OF POSTS AND TAGS !IMPORTANT ##
db.session.add_all(posts_tags)
db.session.commit()
