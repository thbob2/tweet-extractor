import json 

class Tweet():
	
	def __init__(self,id,text,created_at,retweet_count,favorite_count,lang,user_id,coordinates,geo):
		self.id = id
		self.text = text
		self.created_at = created_at 
		self.retweet_count = retweet_count
		self.favorite_count = favorite_count
		self.lang = lang
		self.geo = geo
		self.coordinates = coordinates
		self.user_id = user_id
		self.mention = []
		self.label = ""
		self.tanslation=""
		
	def __str__(self):
		# on ne retourne que le text l'id et la langue 
		return "tweet_id:{} \ncontenu: {} \nlangue du tweet: {}\n".format(self.id,self.text,self.lang)

	def dump(self):
		return {'id': self.id,
				'text': self.text,
				'created_at': self.created_at,
				'retweet_count': self.retweet_count,
				'favorite_count': self.favorite_count,
				'lang': self.lang,
				'geo' : self.geo,
				'coordinates' : self.coordinates,
				'mention': self.mention,
				'label': self.label,
				'user_id': self.user_id
				}

class TweetEncoder(json.JSONEncoder):
	def default(self,obj):
		if isinstance(obj,Tweet):
			return [obj]
		return json.JSONEncoder.default(self,obj)