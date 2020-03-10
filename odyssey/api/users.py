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
	def find_by_username(username):
		found = db.users.find_one({'username': username})
		return User(found['username'], found['password'], found['name'], found['email'])

		

	def hash_password(password):
		return sha256_crypt.hash(password)


	def verify_password(self, password):
		return sha256_crypt.verify(password, self.password)


 