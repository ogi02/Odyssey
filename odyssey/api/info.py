from pymongo import MongoClient

client = MongoClient("mongodb+srv://KelpieG:admin11@clusterodyssey-olnzj.mongodb.net/test?retryWrites=true&w=majority")
db = client.info

class Info:
	def __init__(self, user_id, country_of_residence, country_for_shipping, full_name, address, suite, city, state,
    postal_code, phone_number, facebook, twitter, instagram, webtoon, twitch, youtube, content_type, bio):
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
		self.content_type = content_type
		self.bio = bio

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
			'content_type': self.content_type,
			'bio': self.bio
		}
		result = db.info_collection.insert_one(info)
		print(result)
		return self


values = (
	"5e67e09e97c6eec599b47b96",
	"Belgium",
	"Bulgaria",
	"Gabriela",
	"gj.Druzba 2, bl.240, vh.A, et.5, ap.40",
	"240A",
	"1582",
	"0888543950",
	"Gabriela Baruh",
	"Gabito",
	"gabriela_b",
	None,
	None,
	None,
	"Art, Video",
	"obicham sirene",
	None,
	"mrazq chesun"


)
Info(*values).create()