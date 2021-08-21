import datetime

import mongoengine

class Laptop(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    manifactor = mongoengine.StringField(required=True)
    date_of_release = mongoengine.DateField()
    
    discription = mongoengine.EmbeddedDocumentField()
    extracted_data_ids = mongoengine.ListField()
    mete = {
        'db_alias': 'core',
        'collection': 'laptops'
    }


class Discription(mongoengine.EmbeddedDocument):
    network = mongoengine.StringField()
    body = mongoengine.StringField()
    display = mongoengine.StringField()
    os = mongoengine.StringField()
    cpu = mongoengine.StringField()
    gpu = mongoengine.StringField()
    memory = mongoengine.StringField()
    main_camera = mongoengine.StringField()
    battery = mongoengine.StringField()