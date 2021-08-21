import mongoengine
import datetime

class EData(mongoengine.Document):
    product = mongoengine.ObjectIdField()
    query = mongoengine.StringField()
    begin_date = mongoengine.DateTimeField()
    end_date = mongoengine.DateTimeField()
    total_tweets = mongoengine.IntField()
    positive_tweets = mongoengine.IntField()
    negative_tweets = mongoengine.IntField()
    neutral_tweets = mongoengine.IntField()
    tweets_ids = mongoengine.ListField()

    meta = {
        'db_alias' :'core',
        'collection': 'extracted_data'
    }