import datetime

import mongoengine

class Smartphone(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    manifactor = mongoengine.StringField(required=True)
    date_of_release = mongoengine.DateField()
    
    discription = mongoengine.EmbeddedDocumentField()
    extracted_data = mongoengine
    mete = {
        'db_alias': 'core',
        'collection': 'smartphones'
    }


