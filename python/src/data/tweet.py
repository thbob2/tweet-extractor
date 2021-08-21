import mongoengine



class Score(mongoengine.EmbeddedDocument):
    classification = mongoengine.StringField()
    positivity = mongoengine.FloatField()
    negativity = mongoengine.FloatField()


class Tweet(mongoengine.Document):
    
    t_id = mongoengine.IntField()
    t_text = mongoengine.StringField()
    post_time = mongoengine.DateTimeField()
    lang = mongoengine.StringField()
    retweet_count = mongoengine.IntField()
    fav_count = mongoengine.IntField()
    mentions = mongoengine.ListField()
    label = mongoengine.StringField()

    score = mongoengine.EmbeddedDocument()
    user_id = mongoengine.IntField()

    meta = {
        'db_alias': 'core',
        'collection': 'tweets'
    }