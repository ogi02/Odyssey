import json
import base64
import unittest

from io import BytesIO
from pymongo import MongoClient
from werkzeug.datastructures import FileStorage

from main import app
import database_config

from flask_classes.user import User
from flask_classes.info import Info
from flask_classes.tier import Tier
from flask_classes.post import Post
from flask_classes.active_user import ActiveUser
from flask_classes.creator_specific import CreatorSpecific

class PostTest(unittest.TestCase):

	def get_user_id(self, username):
		user = User.get_from_db(username)

		return user.get('_id')

	def get_post_id(self, username):
		user_id = self.get_user_id(username)

		posts = Post.find_posts_by_user_id(user_id)

		return posts[0].get('_id')

	def get_tier_id(self, username, tiername):
		user_id = self.get_user_id(username)

		tier = Tier.find_by_name(user_id, tiername)

		return tier.get('_id')


	# Register helper function
	def register(self, username, password, name, email):
		return self.app.post(
			"/register",
			data = json.dumps(dict(username = username, password = password, name = name, email = email)),
			content_type = 'application/json',
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
		
	# Verify helper function
	def verify(self, username):
		return self.app.get(
			"/verify/" + username,
			follow_redirects = True
			)

	# Become creator helper function
	def become_creator(self):
		result = {
			'country_of_residence': 'Bulgaria',
			'country_for_shipping': 'Bulgaria',
			'full_name': 'Ognian Baruh',
			'address': None,
			'suite': None,
			'city': 'Sofia',
			'state': None,
			'postal_code': 1407,
			'phone_number': '0882286608',
			'facebook': None,
			'twitter': None,
			'instagram': None,
			'webtoon': None,
			'twitch': 'www.twitch.com',
			'youtube': None,
			'bio':'example bio',
			'working_on': None
		}
		return self.app.post(
			"/becomeCreator",
			data = json.dumps(dict(result = result)),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Create tier helper function
	def create_tier(self, name, price, benefits):
		result = {
			'name': name,
			'price': price,
			'benefits': benefits
		}
		return self.app.post(
			"/createTier",
			data = json.dumps(dict(result = result)),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Subscribe to tier helper function
	def subscribe(self, tier_id, creator_id):
		result = {
			'tier_id': str(tier_id),
			'creator_id': str(creator_id)
		}
		return self.app.post(
			"/chooseTier",
			data = json.dumps(dict(result = result)),
			content_type = 'application/json',
			follow_redirects = True
		)


	# Create post helper function
	def create_post(self, filename, text, restriction_type_id):
		with open(filename, 'rb') as image:
			return self.app.post(
				"/createPost?description=%s&required_id=%s" % (text, restriction_type_id),
				data = dict(image = image),
				content_type = 'multipart/form-data',
				follow_redirects = True
				)

	# Like post helper function
	def like_post(self, post_id):
		return self.app.post(
			"/likePost",
			data = json.dumps(dict(post_id = str(post_id))),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Unlike post helper function
	def unlike_post(self, post_id):
		return self.app.post(
			"/unlikePost",
			data = json.dumps(dict(post_id = str(post_id))),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Get likes on post helper function
	def get_likes_count(self, post_id):
		return self.app.post(
			"/getLikeCount",
			data = json.dumps(dict(post_id = str(post_id))),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Has liked post helper function
	def has_liked_post(self, post_id):
		return self.app.post(
			"/hasLikedPost",
			data = json.dumps(dict(post_id = str(post_id))),
			content_type = 'application/json',
			follow_redirects = True
		)

	# Can view post helper function
	def can_view_post(self, post_id):
		return self.app.post(
			"/canViewPost",
			data = json.dumps(dict(post_id = str(post_id))),
			content_type = 'application/json',
			follow_redirects = True
			)

	# Set Up Class - executed before the first test
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

		Tier.client = MongoClient(database_config.TESTING_DATABASE_URL)
		Tier.db = Tier.client.tier

		Post.client = MongoClient(database_config.TESTING_DATABASE_URL)
		Post.db = Post.client.post

		CreatorSpecific.client = MongoClient(database_config.TESTING_DATABASE_URL)
		CreatorSpecific.db = CreatorSpecific.client.creator_specific

		# create user
		response = self.register(self,
			'_FpCerpd9Z7SIbjmN81Jy_test_profile',
			'12345678',
			'Ognian Baruh',
			'_FpCerpd9Z7SIbjmN81Jy_test_profile@gmail.com'
		)

		self.verify(self, '_FpCerpd9Z7SIbjmN81Jy_test_profile')
		self.login(self, '_FpCerpd9Z7SIbjmN81Jy_test_profile', '12345678')

		# become creator
		response = self.become_creator(self)

		# add tier for subscription
		response = self.create_tier(self, 'Test Tier 1', 10, '["Benefit 1","Benefit 2"]')

	def test_01_create_post_success(self):
		tier_id = self.get_tier_id("_FpCerpd9Z7SIbjmN81Jy_test_profile", "Test Tier 1")
		
		response = self.create_post("./tests/cover.jpeg", "Post description", tier_id)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'_FpCerpd9Z7SIbjmN81Jy_test_profile added a new post', response.data)

	def test_02_create_post_fail_wrong_image_format(self):
		tier_id = self.get_tier_id("_FpCerpd9Z7SIbjmN81Jy_test_profile", "Test Tier 1")

		response = self.create_post("./tests/wrong_cover_image_format.txt", "Post description", tier_id)
		self.assertEqual(response.status_code, 403)
		self.assertIn(b'Allowed extensions: \'pdf\', \'png\', \'jpeg\', \'jpg\', \'gif\'', response.data)

	def test_03_get_likes_after_creation_of_post(self):
		post_id = self.get_post_id("_FpCerpd9Z7SIbjmN81Jy_test_profile")

		response = self.get_likes_count(post_id)
		likes_count = json.loads(response.data.decode('utf8').replace("'", '"')).get('like_count')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(likes_count, 0)

	def test_04_can_view_post_fail_does_not_pass_requirement(self):
		unsubsribed_user = self.register(
			'_FpCerpd9Z7SIbjmN81Jy_test_profile2',
			'12345678',
			'Ognian Baruh',
			'_FpCerpd9Z7SIbjmN81Jy_test_profile2@gmail.com'
		)

		self.verify('_FpCerpd9Z7SIbjmN81Jy_test_profile2')
		self.login('_FpCerpd9Z7SIbjmN81Jy_test_profile2', '12345678')
		
		post_id = self.get_post_id("_FpCerpd9Z7SIbjmN81Jy_test_profile")

		response = self.can_view_post(post_id)
		can_view = json.loads(response.data.decode('utf8').replace("'", '"')).get('view')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(can_view, False)

	def test_05_can_view_post_success(self):
		tier_id = self.get_tier_id("_FpCerpd9Z7SIbjmN81Jy_test_profile", "Test Tier 1")
		creator_id = self.get_user_id("_FpCerpd9Z7SIbjmN81Jy_test_profile")
		subscribe_user = self.subscribe(tier_id, creator_id)
		post_id = self.get_post_id("_FpCerpd9Z7SIbjmN81Jy_test_profile")

		response = self.can_view_post(post_id)
		can_view = json.loads(response.data.decode('utf8').replace("'", '"')).get('view')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(can_view, True)

	def test_06_like_post_success(self):
		post_id = self.get_post_id("_FpCerpd9Z7SIbjmN81Jy_test_profile")

		response = self.like_post(post_id)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"_FpCerpd9Z7SIbjmN81Jy_test_profile2 liked post with id: %s." % str(post_id).encode('utf-8'), response.data)

	def test_07_get_likes_after_user_likes_post(self):
		post_id = self.get_post_id("_FpCerpd9Z7SIbjmN81Jy_test_profile")

		response = self.get_likes_count(post_id)
		likes_count = json.loads(response.data.decode('utf8').replace("'", '"')).get('like_count')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(likes_count, 1)

	def test_08_has_liked_post_true(self):
		post_id = self.get_post_id("_FpCerpd9Z7SIbjmN81Jy_test_profile")

		response = self.has_liked_post(post_id)
		has_liked_post = json.loads(response.data.decode('utf8').replace("'", '"')).get('liked')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(has_liked_post, True)

	def test_09_unlike_post_success(self):
		post_id = self.get_post_id("_FpCerpd9Z7SIbjmN81Jy_test_profile")

		response = self.unlike_post(post_id)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b"_FpCerpd9Z7SIbjmN81Jy_test_profile2 unliked post with id: %s." % str(post_id).encode('utf-8'), response.data)

	def test_10_has_liked_post_false(self):
		post_id = self.get_post_id("_FpCerpd9Z7SIbjmN81Jy_test_profile")

		response = self.has_liked_post(post_id)
		has_liked_post = json.loads(response.data.decode('utf8').replace("'", '"')).get('liked')
		self.assertEqual(response.status_code, 200)
		self.assertEqual(has_liked_post, False)

	# Tear Down Class - executed after the last test
	@classmethod
	def tearDownClass(self):
		User.db.users.remove({})
		Info.db.info_collection.remove({})
		Tier.db.tier_collection.remove({})
		Post.db.posts_collection.remove({})
		CreatorSpecific.db.creator_specifics_collection.remove({})