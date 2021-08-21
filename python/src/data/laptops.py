import datetime

import mongoengine




class LDiscription(mongoengine.EmbeddedDocument):
    network = mongoengine.StringField()
    body = mongoengine.StringField()
    display = mongoengine.StringField()
    os = mongoengine.StringField()
    cpu = mongoengine.StringField()
    gpu = mongoengine.StringField()
    memory = mongoengine.StringField()
    main_camera = mongoengine.StringField()
    battery = mongoengine.StringField()
class Laptop(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    manifactor = mongoengine.StringField(required=True)
    date_of_release = mongoengine.DateField()
    
    discription = mongoengine.EmbeddedDocumentField(LDiscription)
    extracted_data_ids = mongoengine.ListField()
    meta = {
        'db_alias': 'core',
        'collection': 'laptops'
    }


