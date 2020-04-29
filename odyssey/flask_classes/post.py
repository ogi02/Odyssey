from pymongo import ReturnDocument
from pymongo import MongoClient
from bson import ObjectId
from flask_classes.info import Info
from flask_classes.tier import Tier
import datetime

client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.post

class Post:
	def __init__(self, _id, user_id, likes, date, image_path, text, restriction_type_id):
		self._id = _id;
		self.user_id = user_id
		self.likes = likes
		self.date = date
		self.image_path = image_path
		self.text = text
		self.restriction_type_id = restriction_type_id

	def create(self):
		post = {
			'user_id': self.user_id,
			'likes': self.likes,
			'date': self.date,
			'image_path': self.image_path,
			'text': self.text,
			'restriction_type_id': self.restriction_type_id

		}
		result = db.posts_collection.insert_one(post)
		return self
		
	def find_posts_by_user_id(user_id):
		user_id = ObjectId(user_id)
		found = db.posts_collection.find({'user_id': user_id})
		if found:
			return found

	def find_by_id(post_id):
		post_id = ObjectId(post_id)
		found = db.posts_collection.find_one({'_id': post_id})
		if found:
			return found

	def get_likes_count(post_id):
		post_id = ObjectId(post_id)
		found = db.posts_collection.find_one({'_id': post_id})
		if found:
			post = Post(*found)
			return post.likes.len()

	def add_like(user_id, post_id):
		post_id = ObjectId(post_id)
		user_id = ObjectId(post_id)
		db.posts_collection.update_one(
			{'post_id': post_id},
			{"$addToSet": {'likes': user_id}}
		)

	def remove_like(user_id, post_id):
		post_id = ObjectId(post_id)
		user_id = ObjectId(post_id)
		db.posts_collection.update_one(
			{'post_id': post_id},
			{"$pull": {'likes': user_id}}
		)

	def has_liked_post(user_id, post_id):
		post_id = ObjectId(post_id)
		user_id = ObjectId(user_id)
		found = db.posts_collection.find_one({'_id': post_id, 'likes': {"$in": ObjectId(user_id)}})
		if found:
			return True
		return False

	def can_view(user_id, post_id):

		found = Post.find_by_id(post_id)
		creator_id = found.get('user_id')
		restriction_type_id =  found.get('restriction_type_id')
		if not Info.is_patreon(user_id, creator_id):
			return False
				
		current_tier = Tier.find_by_id(Info.get_tier_id(user_id, creator_id))
		minimum_tier = Tier.find_by_id(restriction_type_id)

		if current_tier.get('price') >= minimum_tier.get('price'):
			return True

		return False

