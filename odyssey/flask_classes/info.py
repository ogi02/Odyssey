from bson import ObjectId
from pymongo import MongoClient, ReturnDocument

import database_config

class Info:

	client = MongoClient(database_config.DEVELOPMENT_DATABASE_URL)
	db = client.info

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


	def create(user_id):
		info = {
			'user_id': ObjectId(user_id),
			'country_of_residence': None,
			'shipping_info': {
				'country_for_shipping': None,
				'full_name': None,
				'address': None,
				'suite': None,
				'city': None,
				'state': None,
				'postal_code': None,
				'phone_number': None

			},
			'social_media_links': {
				'facebook': None,
				'twitter': None,
				'instagram': None,
				'webtoon': None,
				'twitch': None,
				'youtube': None
			},
			'bio': None,
			'working_on': None,
			'following': [],
			'patreoning': []
		}
		result = Info.db.info_collection.insert_one(info)

	def update(self):
		Info.db.info_collection.update_one(
			{'user_id': ObjectId(self.user_id)},
			{
				"$set": {
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
					'working_on': self.working_on
				}
			}
		)

	def find_by_user_id(user_id):
		user_id = ObjectId(user_id)
		found = Info.db.info_collection.find_one({'user_id': user_id})
		if found:
			return found


	def is_patreon(user_id, creator_id):
		user_id = ObjectId(user_id)
		creator_id = ObjectId(creator_id)
		found = Info.db.info_collection.find_one({'user_id': user_id,'patreoning': {"$elemMatch": {'creator_id': creator_id}}})
		if found:
			return True
		return False

	def choose_tier(user_id, creator_id, tier_id):
		found = Info.is_patreon(user_id, creator_id)
		if(found):
			Info.db.info_collection.update_one({'user_id': ObjectId(user_id),'patreoning.creator_id': ObjectId(creator_id)}, {"$set": {'patreoning.$.tier_id': ObjectId(tier_id)}})
		else:
			Info.db.info_collection.update_one({'user_id': ObjectId(user_id)}, {"$addToSet": {'patreoning': {'creator_id': ObjectId(creator_id), 'tier_id': ObjectId(tier_id)}}})

	def unsubscribe_from_tier(user_id, creator_id, tier_id):
		Info.db.info_collection.update_one({'user_id': ObjectId(user_id),'patreoning.creator_id': ObjectId(creator_id)}, {"$pull": {'patreoning': {'creator_id': ObjectId(creator_id), 'tier_id': ObjectId(tier_id)}}})

	def get_tier_id(user_id, creator_id):
		user_id = ObjectId(user_id)
		creator_id = ObjectId(creator_id)
		found = Info.db.info_collection.find_one({'user_id': user_id}, {'patreoning': {"$elemMatch": {'creator_id': creator_id}}})
		if found:
			tier_id = found.get('patreoning')[0].get('tier_id')
			return tier_id

	def follow(active_user_id, user_id):
		Info.db.info_collection.update_one({'user_id': active_user_id}, {"$addToSet": {'following': ObjectId(user_id)}})

	def is_following(active_user_id, user_id):
		active_user_id = ObjectId(active_user_id)
		user_id = ObjectId(user_id)
		found = Info.db.info_collection.find_one({'user_id': active_user_id,'following': {"$in": [ObjectId(user_id)]}})
		if found:
			return True
		return False

	def unfollow(active_user_id, user_id):
		active_user_id = ObjectId(active_user_id)
		user_id = ObjectId(user_id)
		Info.db.info_collection.update_one({'user_id': active_user_id}, {"$pull": {'following': ObjectId(user_id)}})

