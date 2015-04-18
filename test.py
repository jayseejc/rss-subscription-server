#!flask/bin/python2
import os
import unittest

from config import basedir
from app import app, db, models
from app.models import User

USERNAME="testuser"
PASSWORD="this is a test"

class TestCase(unittest.TestCase):

	# Run before each test
	def setUp(self):
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'test.db')
		self.app = app.test_client()
		db.create_all()

	# Run after each test
	def tearDown(self):
		db.session.remove()
		db.drop_all()

	def test_user_authentication(self):
		from app import api_models
		# Add the test user
		api_models.create_user(USERNAME, PASSWORD)
		assert api_models.authenticate_user(USERNAME, PASSWORD)

	def test_adding_feed(self):
		from app import api
		# Hope the last user adding test worked. 
		# TODO figure out depending on previous tests
		

if __name__ == '__main__':
	unittest.main()