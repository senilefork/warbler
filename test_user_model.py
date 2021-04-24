"""User model tests."""

# run these tests like:
#
#    python -m unittest test_user_model.py


import os
from unittest import TestCase

from models import db, User, Message, Follows

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


class UserModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()
        Follows.query.delete()

        self.client = app.test_client()

    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no messages & no followers
        self.assertEqual(len(u.messages), 0)
        self.assertEqual(len(u.followers), 0)
        self.assertEqual(u.username, 'testuser')
        self.assertEqual(u.password, 'HASHED_PASSWORD')
        self.assertEqual(u.email, 'test@test.com')

    def test_followed_by(self):
        """does followed by method work?"""

        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(user1, user2)
        db.session.commit()

        self.assertEqual(len(user1.followers), 0)
        user1.followers.append(user2)
        self.assertEqual(len(user1.followers), 1)
        self.assertEqual(user1.followers[0].username, 'testuser2')
        self.assertEqual(user1.is_followed_by(user2), 1)
    
    def test_following(self):

        user1 = User(
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        user2 = User(
            email="test2@test.com",
            username="testuser2",
            password="HASHED_PASSWORD"
        )

        db.session.add(user1, user2)
        db.session.commit()

        self.assertEqual(len(user1.following), 0)
        user1.following.append(user2)
        self.assertEqual(len(user1.following), 1)
        self.assertEqual(user1.following[0].username, 'testuser2')

    def test_user_signup(self):

        user = User.signup(username='testuser', email='test@test.com', password='123', image_url=None)
        db.session.add(user)
        db.session.commit()

        self.assertEqual(user.username, 'testuser')
        self.assertNotEqual(user.password, '123')

    def test_user_authenticate(self):

        user1 = User(
            email="test@test.com",
            username="testuser",
            password="123"
        )

        self.assertEqual(user1.authenticate(user1.username, user1.password), 0)
        self.assertEqual(user1.authenticate(user1.username, 'wrongpassword'), False)





        






