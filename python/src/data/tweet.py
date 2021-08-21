import mongoengine
class Tweet(mongoengine.EmbeddedDocument):

    t_id = mongoengine.IntField()
    t_text = mongoengine.StringField()
    post_time = mongoengine.DateField()
    lang = mongoengine.StringField()
    retweet_count = mongoengine.IntField()
    fav_count = mongoengine.IntField()
    mentions = mongoengine.ListField()
    label = mongoengine.StringField()

    score = mongoengine.EmbeddedDocument()
    user_id = mongoengine.IntField()


class Score(mongoengine.EmbeddedDocument):
    classification = mongoengine.StringFiled()
    positivity = mongoengine.FloatField()
    negativity = mongoengine.FloatField()