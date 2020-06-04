import json
import unittest

from pymongo import MongoClient

from main import app
import database_config

from flask_classes.user import User
from flask_classes.info import Info

class FollowTest(unittest.TestCase):

	# Register helper function
	def register(self, username, password, name, email):
		return self.app.post(
			"/register",
			data = json.dumps(dict(username = username, password = password, name = name, email = email)),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Follow helper function
	def follow(self, profile_name):
		result = {
			'profile_name': profile_name
		}
		return self.app.post(
			"/follow",
			data = json.dumps(dict(result = result)),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Unfollow helper function
	def unfollow(self, profile_name):
		result = {
			'profile_name': profile_name
		}
		return self.app.post(
			"/unfollow",
			data = json.dumps(dict(result = result)),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Is following helper function
	def is_following(self, profile_name):
		result = {
			'profile_name': profile_name
		}
		return self.app.post(
			"/isFollowing",
			data = json.dumps(dict(result = result)),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Set Up - Executed before first test
	@classmethod
	def setUpClass(self):
		# config app
		app.config["TESTING"] = True
		self.app = app.test_client()
		
		# config databases
		User.client = MongoClient(database_config.TESTING_DATABASE_URL)
		User.db = User.client.user

		Info.client = MongoClient(database_config.TESTING_DATABASE_URL)
		Info.db = Info.client.info

		# create user to be followed
		user1 = self.register(self, 
			'_FpCerpd9Z7SIbjmN81Jy_test_profile', 
			'12345678', 
			'Ognian Baruh', 
			'_FpCerpd9Z7SIbjmN81Jy_test_profile@gmail.com')

		# create user that will follow
		user2 = self.register(self, 
			'_FpCerpd9Z7SIbjmN81Jy_test_profile2', 
			'12345678', 
			'Ognian Baruh', 
			'_FpCerpd9Z7SIbjmN81Jy_test_profile1@gmail.com')

	def test_01_is_following_return_false(self):
		response = self.is_following('_FpCerpd9Z7SIbjmN81Jy_test_profile')
		self.assertEqual(response.status_code, 200)
		data = response.data.decode('utf8').replace("'", '"')
		data = json.loads(data)
		self.assertEqual(False, data.get('following'))

	def test_02_follow_user_success(self):
		response = self.follow('_FpCerpd9Z7SIbjmN81Jy_test_profile')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'_FpCerpd9Z7SIbjmN81Jy_test_profile2 started following _FpCerpd9Z7SIbjmN81Jy_test_profile', response.data)

	def test_03_is_following_return_true(self):
		response = self.is_following('_FpCerpd9Z7SIbjmN81Jy_test_profile')
		self.assertEqual(response.status_code, 200)
		data = response.data.decode('utf8').replace("'", '"')
		data = json.loads(data)
		self.assertEqual(True, data.get('following'))

	def test_04_unfollow_user_success(self):
		response = self.unfollow('_FpCerpd9Z7SIbjmN81Jy_test_profile')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'_FpCerpd9Z7SIbjmN81Jy_test_profile2 stopped following _FpCerpd9Z7SIbjmN81Jy_test_profile', response.data)

	def test_05_is_following_return_false(self):
		response = self.is_following('_FpCerpd9Z7SIbjmN81Jy_test_profile')
		self.assertEqual(response.status_code, 200)
		data = response.data.decode('utf8').replace("'", '"')
		data = json.loads(data)
		self.assertEqual(False, data.get('following'))

	@classmethod
	def tearDownClass(cls):
		User.db.users.remove({})
		Info.db.info_collection.remove({})

if __name__ == '__main__':
	unittest.main()