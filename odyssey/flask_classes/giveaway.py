import pymongo
from pymongo import ReturnDocument
from pymongo import MongoClient
from bson import ObjectId
from flask_classes.info import Info
from flask_classes.tier import Tier
import datetime
import random

client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.giveaway

class Giveaway:
	def __init__(self, _id, creator_id, contestants, date, image_path, text, restriction_type_id, is_open, deadline, winner):
		self._id = _id;
		self.creator_id = creator_id
		self.contestants = contestants
		self.date = date
		self.image_path = image_path
		self.text = text
		self.restriction_type_id = restriction_type_id
		self.is_open = is_open
		self.deadline = deadline
		self.winner = winner

	def create(self):
		giveaway = {
			'creator_id': self.creator_id,
			'contestants': [],
			'date': self.date,
			'image_path': self.image_path,
			'text': self.text,
			'restriction_type_id': self.restriction_type_id,
			'is_open': True,
			'deadline': self.deadline,
			'winner': None

		}
		result = db.giveaways_collection.insert_one(giveaway)
		return self
		
	def find_giveaways_by_creator_id(user_id):
		user_id = ObjectId(user_id)
		found = db.giveaways_collection.find({'creator_id': user_id})
		if found:
			return found

	def find_by_id(giveaway_id):
		giveaway_id = ObjectId(giveaway_id)
		found = db.giveaways_collection.find_one({'_id': giveaway_id})
		if found:
			return found

	def get_all_contestants_count(giveaway_id):
		giveaway_id = ObjectId(giveaway_id)
		found = db.giveaways_collection.find_one({'_id': giveaway_id})
		if found:
			return len(found['contestants'])

	def join_giveaway(user_id, giveaway_id):
		giveaway_id = ObjectId(giveaway_id)
		user_id = ObjectId(user_id)
		db.giveaways_collection.update_one(
			{'_id': giveaway_id},
			{"$push": {'contestants': user_id}}
		)

	def has_joined(user_id, giveaway_id):
		giveaway_id = ObjectId(giveaway_id)
		user_id = ObjectId(user_id)
		found = db.giveaways_collection.find_one({'_id': giveaway_id, 'contestants': {"$in": [user_id]}})
		if found:
			return True
		return False

	def close(giveaway_id):
		giveaway_id = ObjectId(giveaway_id)
		db.giveaways_collection.update_one(
			{'_id': giveaway_id},
			{"$set":{'is_open': False}}
		)
		
	def get_random_winner(giveaway_id):
		giveaway_id = ObjectId(giveaway_id)
		found = Giveaway.find_by_id(giveaway_id)
		maxx = Giveaway.get_all_contestants_count(giveaway_id)
		winner_number = random.randint(0, maxx-1)
		return found['contestants'][winner_number]

	def choose_winner(giveaway_id, username):
		giveaway_id = ObjectId(giveaway_id)
		db.giveaways_collection.update_one(
			{'_id': giveaway_id},
			{"$set":{'winner': username}}
		)

	def can_view(user_id, giveaway_id):

		user_id = ObjectId(user_id)
		giveaway_id = ObjectId(giveaway_id)

		found = Giveaway.find_by_id(giveaway_id)
		creator_id = found.get('creator_id')
		restriction_type_id = found.get('restriction_type_id')
		if not Info.is_patreon(user_id, creator_id):
			return False
				
		current_tier = Tier.find_by_id(Info.get_tier_id(user_id, creator_id))
		minimum_tier = Tier.find_by_id(restriction_type_id)

		if current_tier.get('price') >= minimum_tier.get('price'):
			return True
		return False
