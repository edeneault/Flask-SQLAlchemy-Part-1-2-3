"""Seed file to make sample data for pets db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add pets
etienne = User(first_name="Etienne", last_name="Deneault",
               image_url="https://via.placeholder.com/150.png/FFFF00/00000?text=USER_IMG")
leonard = User(first_name="Leonard", last_name="Deneault",
               image_url="https://via.placeholder.com/150.png/FFFF00/00000?text=USER_IMG")
alexandra = User(first_name="Alexandra", last_name="Deneault",
                 image_url="https://via.placeholder.com/150.png/FFFF00/00000?text=USER_IMG")

# Add new objects to session, so they'll persist
db.session.add(etienne)
db.session.add(leonard)
db.session.add(alexandra)

# Commit--otherwise, this never gets saved!
db.session.commit()
