import json
import unittest

from pymongo import MongoClient

from main import app

from flask_classes.user import User
from flask_classes.info import Info

class AuthenticationTest(unittest.TestCase):

	# Set Up Class - Executed before the first test
	@classmethod
	def setUpClass(self):
		# config app
		app.config["TESTING"] = True
		self.app = app.test_client()
		
		# config databases
		User.client = MongoClient("mongodb+srv://Tester:Odyssey2020@cluster0-jyfux.mongodb.net/user?retryWrites=true&w=majority")
		User.db = User.client.user

		Info.client = MongoClient("mongodb+srv://Tester:Odyssey2020@cluster0-jyfux.mongodb.net/user?retryWrites=true&w=majority")
		Info.db = Info.client.info

		# create user
		response = self.register(self,
			'_FpCerpd9Z7SIbjmN81Jy_test_profile',
			'12345678',
			'Ognian Baruh',
			'_FpCerpd9Z7SIbjmN81Jy_test_profile@gmail.com'
		)

	# Tear Down Class - Executed after the last test
	@classmethod
	def tearDownClass(cls):
		User.db.users.remove({})
		Info.db.info_collection.remove({})

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
		response = self.check_username("_FpCerpd9Z7SIbjmN81Jy_free_username")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Username _FpCerpd9Z7SIbjmN81Jy_free_username is not taken', response.data)

	def test_02_validate_username_success_taken(self):
		response = self.check_username("_FpCerpd9Z7SIbjmN81Jy_test_profile")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Username already taken!', response.data)

	def test_03_validate_email_success_free(self):
		response = self.check_email("_FpCerpd9Z7SIbjmN81Jy_free_gmail@email.com")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Email _FpCerpd9Z7SIbjmN81Jy_free_gmail@email.com is not taken', response.data)

	def test_04_validate_email_success_taken(self):
		response = self.check_email("_FpCerpd9Z7SIbjmN81Jy_test_profile@gmail.com")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Email already used!', response.data)

if __name__ == '__main__':
	unittest.main()