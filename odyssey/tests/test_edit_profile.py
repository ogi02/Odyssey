import json
import base64
import unittest

from pymongo import MongoClient

from main import app
import database_config

from io import BytesIO

from flask_classes.user import User
from flask_classes.info import Info

from werkzeug.datastructures import FileStorage

class EditProfileTest(unittest.TestCase):

	# Register helper function
	def register(self, username, password, name, email):
		return self.app.post(
			"/register",
			data = json.dumps(dict(username = username, password = password, name = name, email = email)),
			content_type='application/json',
			)

	# Login helper function
	def login(self, username, password):
		return self.app.post(
			"/login",
			data = json.dumps(dict(username = username, password = password)),
			content_type='application/json',
			)
		
	# Verify helper function
	def verify(self, username):
		return self.app.get(
			"/verify/" + username,
			)

	# Change email/password helper function
	def edit_profile(self, email, password):
		return self.app.post(
			"/editProfile",
			data = json.dumps(dict(email = email, password = password)),
			content_type = 'application/json',
			)

	# Upload new picture
	def upload_picture(self, filename, image_type):
		with open(filename, 'rb') as image:
			return self.app.post(
				"/FpCerpd9Z7SIbjmN81Jy/upload_picture?type=%s" % image_type,
				data = dict(image = image),
				content_type = 'multipart/form-data',
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

		# create user
		response = self.register(self, 
			'_FpCerpd9Z7SIbjmN81Jy_test_profile',
			'12345678',
			'Ognian Baruh',
			'_FpCerpd9Z7SIbjmN81Jy_test_profile@gmail.com'
		)

		self.verify(self, '_FpCerpd9Z7SIbjmN81Jy_test_profile')
		self.login(self, '_FpCerpd9Z7SIbjmN81Jy_test_profile', '12345678')

	def test_01_change_password_only_success(self):
		response = self.edit_profile(None, 'changedpassword')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Changed password for _FpCerpd9Z7SIbjmN81Jy_test_profile ', response.data)

	def test_02_change_email_only_success(self):
		response = self.edit_profile('changed@gmail.com', None)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Changed email for _FpCerpd9Z7SIbjmN81Jy_test_profile ', response.data)

	def test_03_change_email_and_password_success(self):
		response = self.edit_profile('new@gmail.com', 'newpassword')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'Changed email for _FpCerpd9Z7SIbjmN81Jy_test_profile Changed password for _FpCerpd9Z7SIbjmN81Jy_test_profile', response.data)

	def test_04_upload_profile_picture_success(self):
		response = self.upload_picture("./tests/profile.jpeg", "profile")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'New profile picture saved for _FpCerpd9Z7SIbjmN81Jy_test_profile', response.data)

	def test_05_upload_profile_picture_fail_disallowed_extension(self):
		response = self.upload_picture("./tests/wrong_profile_image_format.txt", "profile")
		self.assertEqual(response.status_code, 403)
		self.assertIn(b'Allowed extensions: \'pdf\', \'png\', \'jpeg\', \'jpg\', \'gif\'', response.data)

	def test_06_upload_cover_picture_success(self):
		response = self.upload_picture("./tests/cover.jpeg", "cover")
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'New cover picture saved for _FpCerpd9Z7SIbjmN81Jy_test_profile', response.data)

	def test_07_upload_profile_picture_fail_disallowed_extension(self):
		response = self.upload_picture("./tests/wrong_cover_image_format.txt", "cover")
		self.assertEqual(response.status_code, 403)
		self.assertIn(b'Allowed extensions: \'pdf\', \'png\', \'jpeg\', \'jpg\', \'gif\'', response.data)

	@classmethod
	def tearDownClass(cls):
		User.db.users.remove({})
		Info.db.info_collection.remove({})

if __name__ == '__main__':
	unittest.main()