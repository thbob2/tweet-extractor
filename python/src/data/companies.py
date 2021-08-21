import mongoengine
import datetime as dt

from mongoengine.base import metaclasses


class Company(mongoengine.Document):

    company_name = mongoengine.StringField()
    owner = mongoengine.StringField()
    category = mongoengine.StringField()
    
    extracted_data_ids = mongoengine.ListField()

    meta = {
        'db_alias': 'core',
        'collection': 'companies'
    }