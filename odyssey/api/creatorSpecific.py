from pymongo import MongoClient
from bson import ObjectId
from nestedDict import NestedDictValues
client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.creator_specific
db.creator_specifics.insert_one(
	{
		"Creator_id": ObjectId("5e67e09e97c6eec599b47b96"),
		"Patreons": [[ObjectId("5e67e09e97c6eec599b47b96"), "subscribtion_one"], [ObjectId("5e67e09e97c6eec599b47b96"), "subscribtion_one"]]
	}
)
