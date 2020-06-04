from bson import ObjectId
from passlib.hash import sha256_crypt
from pymongo import MongoClient, ReturnDocument

import database_config

class User:

	client = MongoClient(database_config.DEVELOPMENT_DATABASE_URL)
	db = client.user

	def __init__(self, _id, username, password, name, email, role):
		self._id = _id
		self.username = username
		self.password = password
		self.name = name
		self.email = email
		self.role = role

	def create(self):
		user = {
			'username': self.username,
			'password': self.password,
			'name': self.name,
			'email': self.email,
			'role': "user"
		}
		result = User.db.users.insert_one(user)
		return self

	def create_creator(self):
		user = {
			'username': self.username,
			'password': self.password,
			'name': self.name,
			'email': self.email,
			'role': "creator"
		}
		result = User.db.users.insert_one(user)
		return self

	def update_to_creator(username):
		found = User.db.users.find_one_and_update(
			{'username': username},
			{"$set": {'role': "creator"}},
			return_document=ReturnDocument.AFTER
		)

	def find_by_username(username):
		found = User.db.users.find_one({'username': username})
		if found:
			return User(*found.values())

	def find_by_email(email):
		found = User.db.users.find_one({'email': email})
		if found:
			return User(*found.values())

	def find_by_id(user_id):
		user_id = ObjectId(user_id)
		found = User.db.users.find_one({'_id': user_id})
		if found:
			return found

	def get_from_db(username):
		found = User.db.users.find_one({'username': username})
		if found:
			return found

	def get_searched_usernames(value, excluded):
		username = '^' + value
		found = User.db.users.find(
			{'$and': [
				{'username': {'$regex': username, '$options': 'i'}},
				{'username': {'$ne': excluded}}
			]}
		).limit(7)
		if found:
			return [User(*user.values()).username for user in found]

	def hash_password(password):
		return sha256_crypt.hash(password)

	def verify_password(self, password):
		return sha256_crypt.verify(password, self.password)

	def change_password(username, new_password):
		new_password = User.hash_password(new_password)
		change = User.db.users.find_one_and_update(
			{'username': username},
			{"$set": {'password': new_password}},
			return_document=ReturnDocument.AFTER
		)

	def change_email(username, new_email):
		change = User.db.users.find_one_and_update(
			{'username': username},
			{"$set": {'email': new_email}},
			return_document=ReturnDocument.AFTER
		)




