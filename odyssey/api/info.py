from pymongo import MongoClient
from bson import ObjectId
from nestedDict import NestedDictValues
from pymongo import ReturnDocument
client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.info
class Info:
	def __init__(self, _id, user_id, country_of_residence, country_for_shipping, full_name, address, suite, city, state,
	postal_code, phone_number, facebook, twitter, instagram, webtoon, twitch, youtube, bio, working_on, following, patreoning):
		self._id = _id
		self.user_id = user_id
		self.country_of_residence = country_of_residence
		self.country_for_shipping = country_for_shipping
		self.full_name = full_name
		self.address = address
		self.suite = suite
		self.city = city
		self.state = state
		self.postal_code = postal_code
		self.phone_number = phone_number
		self.facebook = facebook
		self.twitter = twitter
		self.instagram = instagram
		self.webtoon = webtoon
		self.twitch = twitch
		self.youtube = youtube
		self.bio = bio
		self.working_on = working_on
		self.following = following
		self.patreoning = patreoning


	def create(self):
		info = {
			'user_id': self.user_id,
			'country_of_residence': self.country_of_residence,
			'shipping_info': {
				'country_for_shipping': self.country_for_shipping,
				'full_name': self.full_name,
				'address': self.address,
				'suite': self.suite,
				'city': self.city,
				'state': self.state,
				'postal_code': self.postal_code,
				'phone_number': self.phone_number

			},
			'social_media_links': {
				'facebook': self.facebook,
				'twitter': self.twitter,
				'instagram': self.instagram,
				'webtoon': self.webtoon,
				'twitch': self.twitch,
				'youtube': self.youtube
			},
			'bio': self.bio,
			'working_on': self.working_on,
			'following': [[]],
			'patreoning': [[]]
		}
		result = db.info_collection.insert_one(info)
		return self

	
	def find_by_user_id(user_id):
		user_id = ObjectId(user_id)
		found = db.info_collection.find_one({'user_id': user_id})
		if found:
			return found

	def become_patreon(self, creator_id, tier_id):
		found = db.info_collection.find_one_and_update({'user_id': self.user_id}, {"$addToSet": {'patreoning': [[ObjectId(creator_id), ObjectId(tier_id)]]}}, return_document=ReturnDocument.AFTER)



