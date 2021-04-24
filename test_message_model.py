"""Message model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows, Likes

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_message_model(self):
        """Test basic message model"""
        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        ) 

        db.session.add(user1)
        db.session.commit()

        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(user2)
        db.session.commit()

        message = Message(
            text="This is a test message",
            timestamp=None,
            user_id=f"{user1.id}",
        )

        db.session.add(message)
        db.session.commit()

        like = Likes(
            user_id = f'{user2.id}',
            message_id = f'{message.id}'
        )

        db.session.add(like)
        db.session.commit()

        self.assertEqual(message.text, 'This is a test message')
        self.assertEqual(len(user1.messages), 1)
        self.assertEqual(len(user2.likes), 1)

    