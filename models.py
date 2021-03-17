from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


DEFAULT_IMAGE_URL = "https://via.placeholder.com/150.png/FFFF00/00000?text=USER_IMG"


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(30), nullable=True)

    image_url = db.Column(db.String(200), nullable=False,
                          default=DEFAULT_IMAGE_URL)

    def __repr__(self):
        p = self
        return f"<User id={p.id} first_name={p.first_name} last_name={p.last_name} image_url={p.image_url}>"

    def full_name(self):
        """Return full name of user."""

        return f"{self.first_name} {self.last_name}"
