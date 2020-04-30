import json
import unittest

from pymongo import MongoClient

from main import app

from flask_classes.user import User

class AuthenticationTest(unittest.TestCase):

	# Set Up Class - Executed before the first test
	@classmethod
	def setUpClass(self):
		# config app
		app.config["TESTING"] = True
		self.app = app.test_client()
		
		# config database
		User.client = MongoClient("mongodb+srv://Tester:Odyssey2020@cluster0-jyfux.mongodb.net/user?retryWrites=true&w=majority")
		User.db = User.client.user

		# create user
		response = self.register(self, 'ogi', '12345678', 'Ognian Baruh', 'ogi@gmail.com')

	# Tear Down Class - Executed after the last test
	@classmethod
	def tearDownClass(cls):
		User.db.users.remove({})

	# Set Up - Executed before each test
	def setUp(self):
		pass

	# Tear Down - Executed after each test
	def tearDown(self):
		pass

	# Register helper function
	def register(self, username, password, name, email):
		return self.app.post(
			"/register",
			data = json.dumps(dict(username = username, password = password, name = name, email = email)),
			content_type = 'application/json',
			follow_redirects = True
			)

	def check_username(self, username):
		return self.app.post(
			"/FpCerpd9Z7SIbjmN81Jy/username",
			data = json.dumps(dict(username = username)),
			content_type = 'application/json',
			follow_redirects = True
			)

	def check_email(self, email):
		return self.app.post(
			"/FpCerpd9Z7SIbjmN81Jy/email",
			data = json.dumps(dict(email = email)),
			content_type = 'application/json',
			follow_redirects = True
			)

	def test_01_validate_username_success_free(self):
		response = self.check_username("freeusername")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Username freeusername is not taken', response.data)

	def test_02_validate_username_success_taken(self):
		response = self.check_username("ogi")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'An account with such username already exists', response.data)

	def test_03_validate_email_success_free(self):
		response = self.check_email("free@email.com")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Email free@email.com is not taken', response.data)

	def test_04_validate_email_success_taken(self):
		response = self.check_email("ogi@gmail.com")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'An account with such email already exists', response.data)

if __name__ == '__main__':
	unittest.main()