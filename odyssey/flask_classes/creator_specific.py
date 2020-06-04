from bson import ObjectId
from pymongo import MongoClient, ReturnDocument

import database_config

class CreatorSpecific:

	client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
	db = client.creator_specific

	def __init__(self, _id, user_id, followers, patreons, content_type):
		self._id = _id;
		self.user_id = user_id
		self.followers = followers
		self.patreons = patreons
		self.content_type = content_type

	def create(self):
		creator_specific = {
			'user_id': self.user_id,
			'followers': [],
			'patreons': [[]],
			'content_type': self.content_type

		}
		result = CreatorSpecific.db.creator_specifics_collection.insert_one(creator_specific)
		return self
		
	def find_by_user_id(user_id):
		user_id = ObjectId(user_id)
		found = CreatorSpecific.db.creator_specifics_collection.find_one({'user_id': user_id})
		if found:
			return found

	def get_follower_count(user_id):
		user_id = ObjectId(user_id)
		found = CreatorSpecific.db.creator_specifics_collection.find_one({'user_id': user_id})
		if found:
			info = Info(*found)
			return info.followers.len()

	def get_patreons_count(user_id):
		user_id = ObjectId(user_id)
		found = CreatorSpecific.db.creator_specifics_collection.find_one({'user_id': user_id})
		if found:
			info = Info(*found)
			return info.patreons.len()