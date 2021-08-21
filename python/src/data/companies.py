import mongoengine
import datetime as dt


class Company(mongoengine.Document):

    company_name = mongoengine.StringField()
    owner = mongoengine.StringFiled()
    category = mongoengine.StringField()
    