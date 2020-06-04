import json
import unittest

from pymongo import MongoClient

from main import app
import database_config

from flask_classes.user import User
from flask_classes.info import Info

class AuthenticationTest(unittest.TestCase):

	# Set Up - Executed before each test
	def setUp(self):
		app.config["TESTING"] = True
		self.app = app.test_client()
		# config databases
		User.client = MongoClient(database_config.TESTING_DATABASE_URL)
		User.db = User.client.user

		Info.client = MongoClient(database_config.TESTING_DATABASE_URL)
		Info.db = Info.client.info

	# Tear Down - Executed after each test
	def tearDown(self):
		pass

	# Register helper function
	def register(self, username, password, name, email):
		return self.app.post(
			"/register",
			data = json.dumps(dict(username = username, password = password, name = name, email = email)),
			content_type='application/json',
			follow_redirects = True
			)

	# Login helper function
	def login(self, username, password):
		return self.app.post(
			"/login",
			data = json.dumps(dict(username = username, password = password)),
			content_type='application/json',
			follow_redirects = True
			)

	# Logout helper function
	def logout(self):
		return self.app.get(
			"/logout",
			follow_redirects = True
			)

	def test_01_main_page(self):
		response = self.app.get('/', follow_redirects=True)
		self.assertEqual(response.status_code, 200)

	def test_02_valid_user_registration(self):
		response = self.register(
			'_FpCerpd9Z7SIbjmN81Jy_test_profile',
			'12345678',
			'Ognian Baruh',
			'_FpCerpd9Z7SIbjmN81Jy_test_profile@baruh.net'
		)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Registration successful', response.data)

	def test_03_invalid_user_registration_duplicate_username(self):
		response = self.register(
			'_FpCerpd9Z7SIbjmN81Jy_test_profile',
			'12345678',
			'Ognian Baruh',
			'_FpCerpd9Z7SIbjmN81Jy_test_profile_2@baruh.net'
		)
		self.assertEqual(response.status_code, 403)
		self.assertIn(b'Duplicate username: _FpCerpd9Z7SIbjmN81Jy_test_profile', response.data)

	def test_04_invalid_user_registration_duplicate_email(self):
		response = self.register(
			'_FpCerpd9Z7SIbjmN81Jy_test_profile_2',
			'12345678',
			'Ognian Baruh',
			'_FpCerpd9Z7SIbjmN81Jy_test_profile@baruh.net'
		)
		self.assertEqual(response.status_code, 403)
		self.assertIn(b'Duplicate email: _FpCerpd9Z7SIbjmN81Jy_test_profile@baruh.net', response.data)

	def test_05_valid_user_login(self):
		response = self.login('_FpCerpd9Z7SIbjmN81Jy_test_profile', '12345678')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'_FpCerpd9Z7SIbjmN81Jy_test_profile logged in successfully', response.data)

	def test_06_invalid_user_login_username_does_not_exist(self):
		response = self.login('invalid', '12345678')
		self.assertEqual(response.status_code, 403)
		self.assertIn(b'Incorrect username or password', response.data)

	def test_07_invalid_user_login_incorrect_password(self):
		response = self.login('_FpCerpd9Z7SIbjmN81Jy_test_profile', 'incorrect')
		self.assertEqual(response.status_code, 403)
		self.assertIn(b'Incorrect username or password', response.data)

	def test_08_valid_user_logout(self):
		response = self.logout()
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'_FpCerpd9Z7SIbjmN81Jy_test_profile logged out', response.data)

	@classmethod
	def tearDownClass(cls):
		User.db.users.remove({})
		Info.db.info_collection.remove({})

if __name__ == '__main__':
	unittest.main()