import datetime

import mongoengine




class SDiscription(mongoengine.EmbeddedDocument):
    network = mongoengine.StringField()
    body = mongoengine.StringField()
    display = mongoengine.StringField()
    os = mongoengine.StringField()
    cpu = mongoengine.StringField()
    gpu = mongoengine.StringField()
    memory = mongoengine.StringField()
    main_camera = mongoengine.StringField()
    selfie_camera = mongoengine.StringField()
    battery = mongoengine.StringField()
class Smartphone(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    manifactor = mongoengine.StringField(required=True)
    date_of_release = mongoengine.StringField()
    
    discription = mongoengine.EmbeddedDocumentField(SDiscription)
    extracted_data_ids = mongoengine.ListField()
    
    meta = {
        'db_alias': 'core',
        'collection': 'smartphones'
    }

