import json 
import httpx
class Tweet():
	
	def __init__(self,id,text,created_at,retweet_count,favorite_count,lang,user_id,coordinates,geo,label="",note={}):
		timout = httpx.Timeout(30)		
		
		#translator = Translator(timeout=timout)
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
		self.label = label
		self.note = note
		#result = translator.translate(text,dest="en")
		#print("translating text")
		self.translation=""
		#print("object created")
	
	def __str__(self):
		# on ne retourne que le text l'id et la langue 
		return "tweet_id:{} \ncontenu: {} \nlangue du tweet: {}\n".format(self.id,self.text,self.lang)

	def dumps(self):
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
				'note' : self.note,
				'user_id': self.user_id,
				'text_translation': self.translation
				}

class TweetEncoder(json.JSONEncoder):
	def default(self,obj):
		if isinstance(obj,Tweet):
			return [obj]
		return json.JSONEncoder.default(self,obj)