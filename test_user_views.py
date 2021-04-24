"""Message View tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_message_views.py


import os
from unittest import TestCase

from models import db, connect_db, Message, User

# BEFORE we import our app, let's set an environmental variable
# to use a different database for tests (we need to do this
# before we import our app, since that will have already
# connected to the database

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"


# Now we can import app

from app import app, CURR_USER_KEY

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()

# Don't have WTForms use CSRF at all, since it's a pain to test

app.config['WTF_CSRF_ENABLED'] = False

class MessageViewTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        User.query.delete()
        Message.query.delete()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None)
        
        self.testuser2 = User.signup(username="testuser2",
                                    email="test2@test.com",
                                    password="testuser",
                                    image_url=None)

        self.testuser3 = User.signup(username="testuser3",
                                    email="test3@test.com",
                                    password="testuser",
                                    image_url=None)

        db.session.commit()

    def test_list_users(self):
        """Test list_users view"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f'/users?={self.testuser.username}')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<img src="/static/images/default-pic.png" alt="Image for testuser" class="card-image">', html)

            resp = c.get('/users')
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<img src="/static/images/default-pic.png" alt="Image for testuser" class="card-image">', html)

    def test_user_profile(self):
        """Test for user info and messages on page"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            
            resp = c.get(f'/users/{self.testuser.id}')
            #msg = c.post("/messages/new", data={"text": "Hello"})
            #html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            #self.assertIn('hello', html)
    
    def test_user_following(self):
        """Test user following route"""

        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
                self.testuser.following.append(self.testuser2)
                followed = self.testuser.following[0].username
                
            
            resp = c.get(f'/users/{self.testuser.id}/following')
            self.assertEqual(resp.status_code, 200)
            self.assertEqual(len(self.testuser.following) , 1)
            self.assertEqual(followed, 'testuser2')


    # def test_user_followers(self):
    #     """Test follow user post request"""

    #     # first test the current number of users that currentuser is following
    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id
    #             followed = self.testuser.following #this is to load the .following attribute on to the testuser instance
    #             testuser2 = self.testuser2.id
                
            
    #         resp = c.get(f'/users/{self.testuser.id}/following')
    #         self.assertEqual(len(self.testuser.following) , 0)
            
    #         resp = c.post(f'/users/follow/{testuser2}', data = {"id" : f"{testuser2}"})

    #         self.assertEqual(len(self.testuser.following) , 1)
    
    # def test_stop_following(self):

    # def test_update_profile(self):
    #     """Test update page/route"""

    #     with self.client as c:
    #         with c.session_transaction() as sess:
    #             sess[CURR_USER_KEY] = self.testuser.id

    #         resp = c.post(f'/users/profile/{self.testuser.id}', data = {"username" : "blue"})
    #         self.assertEqual(self.testuser.username, 'blue')






    













            


            


