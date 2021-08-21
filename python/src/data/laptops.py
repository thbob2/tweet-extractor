import datetime

import mongoengine

class Laptop(mongoengine.Document):
    name = mongoengine.StringField(required=True)
    manifactor = mongoengine.StringField(required=True)
    date_of_release = mongoengine.DateField()
    
    discription = mongoengine.EmbeddedDocumentField()

    mete = {
        'db_alias': 'core',
        'collection': 'laptops'
    }


class Discription(mongoengine.EmbeddedDocument):
    pass