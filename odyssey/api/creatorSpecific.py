from pymongo import MongoClient
from bson import ObjectId
from nestedDict import NestedDictValues
from pymongo import ReturnDocument
client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.creator_specific
class CreatorSpecific:
	def __init__(self, _id, user_id, followers, patreons, content_type, tiers):
		
