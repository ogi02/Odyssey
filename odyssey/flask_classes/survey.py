import pymongo
from pymongo import ReturnDocument
from pymongo import MongoClient
from bson import ObjectId
import datetime
import random

client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.survey

class Survey:
	def __init__(self, _id, creator_id, votes, date, image_path, text, restriction_type_id, options, is_open, type, deadline, winner):
		self._id = _id;
		self.creator_id = creator_id
		self.votes = votes
		self.date = date
		self.image_path = image_path
		self.text = text
		self.restriction_type_id = restriction_type_id
		self.options = options
		self.is_open = is_open
		self.type = type
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
			'options': [],
			'is_open': True,
			'type': self.type,
			'deadline': self.deadline,
			'winner': None

		}
		result = db.surveys_collection.insert_one(survey)
		return self
		
	def find_surveys_by_user_id(user_id):
		user_id = ObjectId(user_id)
		found = db.surveys_collection.find({'user_id': user_id})
		if found:
			return found

	def find_by_id(survey_id):
		survey_id = ObjectId(survery_id)
		found = db.surveys_collection.find_one({'_id': survery_id})
		if found:
			return found

	def get_votes_count_by_option(survery_id, option_number):
		survery_id = ObjectId(survery_id)
		found = db.surveys_collection.count({'_id': survery_id, 'votes':{"$elemMatch": {'number': option_number}}})
		if found:
			return foundx

	def get_all_votes_count(survery_id):
		survery_id = ObjectId(survery_id)
		found = db.posts_collection.find_one({'id': survery_id})
		if found:
			survey = Survey(*found)
			return survey.votes.len()

	def vote(user_id, survery_id, option_number):
		survery_id = ObjectId(survery_id)
		user_id = ObjectId(user_id)
		db.surveys_collection.update_one(
			{'survery_id': survery_id},
			{"$addToSet": {'votes': {'user_id': user_id, 'vote': option_number}}}
		)

	def has_voted(user_id, survery_id):
		survery_id = ObjectId(survery_id)
		user_id = ObjectId(user_id)
		if db.surveys_collection.find_one({'survery_id': survery_id, 'votes': {"$in": user_id}}):
			return True
		return False

	def close(user_id, survery_id):
		survery_id = ObjectId(survery_id)
		user_id = ObjectId(user_id)
		db.surveys_collection.update_one(
			{'survery_id': survery_id},
			{'is_open': False}
		)
	def get_random_winner(survey_id):
		survery_id = ObjectId(survery_id)
		user_id = ObjectId(user_id)
		survey = Survey(Survey.find_by_id(survery_id))
		max = survey.votes.len()
		winner_number = random.randint(0, max)
		return survey.votes[winner_number]


	def get_choose_winner(survery_id, user_id):
		survery_id = ObjectId(survery_id)
		user_id = ObjectId(user_id)
		db.surveys_collection.update_one(
			{'survery_id': survery_id},
			{'winner': user_id}
		)


Survey(None, ObjectId("5e7262878494818ae5350a57"), None, None, None, None, None, None, True, None, None, None).create()