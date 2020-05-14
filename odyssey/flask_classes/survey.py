import pymongo
from pymongo import ReturnDocument
from pymongo import MongoClient
from bson import ObjectId
from flask_classes.info import Info
from flask_classes.tier import Tier
import datetime
import random

client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.survey

class Survey:
	def __init__(self, _id, creator_id, votes, date, image_path, text, restriction_type_id, options, is_open, deadline, winner):
		self._id = _id;
		self.creator_id = creator_id
		self.votes = votes
		self.date = date
		self.image_path = image_path
		self.text = text
		self.restriction_type_id = restriction_type_id
		self.options = options
		self.is_open = is_open
		self.deadline = deadline
		self.winner = winner

	def create(self):
		survey = {
			'creator_id': self.creator_id,
			'votes': [],
			'date': self.date,
			'image_path': self.image_path,
			'text': self.text,
			'restriction_type_id': self.restriction_type_id,
			'options': self.options,
			'is_open': True,
			'deadline': self.deadline,
			'winner': None
		}
		result = db.surveys_collection.insert_one(survey)
		return self
		
	def find_surveys_by_creator_id(user_id):
		user_id = ObjectId(user_id)
		found = db.surveys_collection.find({'creator_id': user_id})
		if found:
			return found

	def find_by_id(survey_id):
		survey_id = ObjectId(survey_id)
		found = db.surveys_collection.find_one({'_id': survey_id})
		if found:
			return found

	def get_votes_count_by_option(survey_id, option_number):
		survey_id = ObjectId(survey_id)
		found = db.surveys_collection.find_one({'_id': survey_id})
		if found:
			count = 0
			for f in found['votes']:
				if int(f['vote']) == option_number:
					count = count + 1
			return count

	def get_all_votes_count(survey_id):
		survey_id = ObjectId(survey_id)
		found = db.surveys_collection.find_one({'_id': survey_id})
		if found:
			return len(found['votes'])

	def vote(user_id, survey_id, option_number):
		survey_id = ObjectId(survey_id)
		user_id = ObjectId(user_id)
		db.surveys_collection.update_one(
			{'_id': survey_id},
			{"$addToSet": {'votes': {'user_id': user_id, 'vote': option_number}}}
		)

	def has_voted(user_id, survey_id):
		survey_id = ObjectId(survey_id)
		user_id = ObjectId(user_id)
		found = db.surveys_collection.find_one({'_id': survey_id, 'votes': {"$elemMatch": {'user_id': user_id}}})
		if found:
			return True
		return False

	def close(survey_id):
		survey_id = ObjectId(survey_id)
		db.surveys_collection.update_one(
			{'_id': survey_id},
			{"$set":{'is_open': False}}
		)
		
	def get_wining_option(survey_id):
		survey_id = ObjectId(survey_id)
		found = Survey.find_by_id(survey_id)
		win = None
		size = len(found['options'])
		maximum = 0
		for i in range(0,size):
			option_votes = Survey.get_votes_count_by_option(survey_id, i)
			if option_votes:
				if Survey.get_votes_count_by_option(survey_id, i) > maximum:
					win = found.get('options')[i]
					maximum = Survey.get_votes_count_by_option(survey_id, i)
		db.surveys_collection.update_one(
			{'_id': survey_id},
			{"$set":{'winner': win}}
		)
		return win

	def can_view(user_id, survey_id):

		found = Survey.find_by_id(ObjectId(survey_id))
		creator_id = found.get('creator_id')
		restriction_type_id = found.get('restriction_type_id')
		if not Info.is_patreon(user_id, creator_id):
			return False
				
		current_tier = Tier.find_by_id(Info.get_tier_id(user_id, creator_id))
		minimum_tier = Tier.find_by_id(restriction_type_id)

		if int(current_tier.get('price')) >= int(minimum_tier.get('price')):
			return True
		return False