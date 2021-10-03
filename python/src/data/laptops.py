import datetime

import mongoengine




class LDiscription(mongoengine.EmbeddedDocument):
    network = mongoengine.StringField()
    body = mongoengine.StringField()
    display = mongoengine.StringField()
    os = mongoengine.StringField()
    cpu = mongoengine.StringField()
    gpu = mongoengine.StringField()
    ram = mongoengine.StringField()
    storage =  mongoengine.StringField()
    webcam = mongoengine.StringField()
    battery = mongoengine.StringField()
    other_features = mongoengine.StringField()
class Laptop(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    manifactor = mongoengine.StringField(required=True)
    date_of_release = mongoengine.StringField()
    
    discription = mongoengine.EmbeddedDocumentField(LDiscription)
    extracted_data_ids = mongoengine.ListField()
    meta = {
        'db_alias': 'core',
        'collection': 'laptops'
    }


