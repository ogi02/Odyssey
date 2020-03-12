from flask import jsonify
from pymongo import MongoClient
from passlib.hash import sha256_crypt

client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.user

class User:
	def __init__(self, username, password, name, email):
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
		print(result)
		return self

	def all():
		output = []
		for user in db.users.find():
			output.append({'username': user['username'], 'password': user['password'], 'name': user['name'], 'email': user['email']})

		return jsonify({'result': output})

	def find_by_username(username):
		found = db.users.find_one({'username': username})
		if found:
			return User(found['username'], found['password'], found['name'], found['email'])

	def find_by_email(email):
		found = db.users.find_one({'email': email})
		if found:
			return User(found['username'], found['password'], found['name'], found['email'])

	def hash_password(password):
		return sha256_crypt.hash(password)


	def verify_password(self, password):
		return sha256_crypt.verify(password, self.password)
		

 