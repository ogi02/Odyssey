from pymongo import MongoClient
from bson import ObjectId
from pymongo import ReturnDocument

client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.tier
class Tier:
	def __init__(self, _id, user_id, benefits, price, name):
		self._id = _id
		self.user_id = user_id
		self.benefits = benefits
		self.price = price
		self.name = name

	def create(self):
		tier = {
			'user_id': self.user_id,
			'name': self.name,
			'benefits': self.benefits,
			'price': self.price
		}
		result = db.tier_collection.insert_one(tier)
		return self
	
	def find_all_by_user_id(user_id):
		user_id = ObjectId(user_id)
		found = db.tier_collection.find({'user_id': user_id})
		if found:
			return found
			
	def find_by_name(user_id, name):
		user_id = ObjectId(user_id)
		found = db.tier_collection.find_one({'user_id': user_id, 'name': name})
		if found:
			return found

	def find_by_id(tier_id):
		tier_id = ObjectId(tier_id)
		found = db.tier_collection.find_one({'_id': tier_id})
		if found:
			return found

	def delete_tier(tier_id):
		tier_id = ObjectId(tier_id)
		db.tier_collection.delete_one({'_id': tier_id})
		
