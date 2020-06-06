import json
import unittest

from pymongo import MongoClient

from main import app
import database_config

from flask_classes.user import User
from flask_classes.info import Info
from flask_classes.tier import Tier
from flask_classes.creator_specific import CreatorSpecific

class FollowTest(unittest.TestCase):

	# Register helper function
	def register(self, username, password, name, email):
		return self.app.post(
			"/register",
			data = json.dumps(dict(username = username, password = password, name = name, email = email)),
			content_type = 'application/json',
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
		)

	# Unsubscribe to tier helper function
	def unsubscribe(self, tier_id, creator_id):
		result = {
			'tier_id': str(tier_id),
			'creator_id': str(creator_id)
		}
		return self.app.post(
			"/removeTier",
			data = json.dumps(dict(result = result)),
			content_type = 'application/json',
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

		Tier.client = MongoClient(database_config.TESTING_DATABASE_URL)
		Tier.db = Tier.client.tier

		CreatorSpecific.client = MongoClient(database_config.TESTING_DATABASE_URL)
		CreatorSpecific.db = CreatorSpecific.client.creator_specific

		# Creator
		self.register(self, 
			'_FpCerpd9Z7SIbjmN81Jy_test_profile', 
			'12345678', 
			'Ognian Baruh', 
			'_FpCerpd9Z7SIbjmN81Jy_test_profile@gmail.com'
		)
		self.verify(self, '_FpCerpd9Z7SIbjmN81Jy_test_profile')
		self.login(self, '_FpCerpd9Z7SIbjmN81Jy_test_profile', '12345678')

	def test_01_become_creator_success(self):
		response = self.become_creator()
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'_FpCerpd9Z7SIbjmN81Jy_test_profile became a creator', response.data)

	def test_02_create_tier_success(self):
		response = self.create_tier('Test Tier 1', 10, '["Benefit 1","Benefit 2"]')
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'_FpCerpd9Z7SIbjmN81Jy_test_profile added a new tier named Test Tier 1', response.data)

	def test_03_subscribe_to_tier_success(self):
		# User
		self.register( 
			'_FpCerpd9Z7SIbjmN81Jy_test_profile2', 
			'12345678', 
			'Ognian Baruh', 
			'_FpCerpd9Z7SIbjmN81Jy_test_profile1@gmail.com'
		)

		self.verify('_FpCerpd9Z7SIbjmN81Jy_test_profile2')
		self.login('_FpCerpd9Z7SIbjmN81Jy_test_profile2', '12345678')

		creator_id = User.get_from_db('_FpCerpd9Z7SIbjmN81Jy_test_profile').get('_id')
		tier_id = Tier.find_by_name(creator_id, 'Test Tier 1').get('_id')
		response = self.subscribe(tier_id, creator_id)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'_FpCerpd9Z7SIbjmN81Jy_test_profile2 subscribed to tier Test Tier 1', response.data)

	def test_04_unsubscribe_to_tier_success(self):
		creator_id = User.get_from_db('_FpCerpd9Z7SIbjmN81Jy_test_profile').get('_id')
		tier_id = Tier.find_by_name(creator_id, 'Test Tier 1').get('_id')
		response = self.unsubscribe(tier_id, creator_id)
		self.assertEqual(response.status_code, 200)
		self.assertIn(b'_FpCerpd9Z7SIbjmN81Jy_test_profile2 unsubscribed from tier Test Tier 1', response.data)

	@classmethod
	def tearDownClass(cls):
		User.db.users.remove({})
		Info.db.info_collection.remove({})
		Tier.db.tier_collection.remove({})
		CreatorSpecific.db.creator_specifics_collection.remove({})

if __name__ == '__main__':
	unittest.main()