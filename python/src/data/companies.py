import mongoengine
import datetime as dt





class Company(mongoengine.Document):

    name = mongoengine.StringField()
    owner = mongoengine.StringField()
    category = mongoengine.StringField()
    net_worth = mongoengine.StringField()
    extracted_data_ids = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'companies'
    }