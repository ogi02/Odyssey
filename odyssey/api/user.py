from flask import jsonify
from pymongo import MongoClient
from passlib.hash import sha256_crypt
from bson import ObjectId

client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.user

class User:
	def __init__(self, _id, username, password, name, email):
		self._id = _id
		self.username = username
		self.password = password
		self.name = name
		self.email = email

	def create(self):
		user = {
			'username': self.username,
			'password': self.password,
			'name': self.name,
			'email': self.email
		}
		result = db.users.insert_one(user)
		return self

	def find_by_username(username):
		found = db.users.find_one({'username': username})
		if found:
			return User(*found.values())

	def find_by_email(email):
		found = db.users.find_one({'email': email})
		if found:
			return User(*found.values())

	def find_by_id(user_id):
		user_id = ObjectId(user_id)
		found = db.users.find_one({'_id': user_id})
		if found:
			return User(*found.values())

	def hash_password(password):
		return sha256_crypt.hash(password)


	def verify_password(self, password):
		return sha256_crypt.verify(password, self.password)
