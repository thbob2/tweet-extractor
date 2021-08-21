from typing import List, Optional
import datetime
import bson
from data.companies import Company
from data.laptops import Laptop
from data.laptops import LDiscription
from data.smartphones import Smartphone
from data.smartphones import SDiscription
from data.extracted_data import EData

def create_smartphone(name,manifactor,release,discription):
    phone = Smartphone()
    phone.name = name
    phone.manifactor = manifactor
    phone.date_of_release = release
    phone.discription = discription
    phone.save()
    return phone

def find_phone_by_name(name) :
    phone = Smartphone.objects(name=name).first()
    return phone

def add_phone_data(name,bdate,edate,total,pos,neg,neut):
    
    doc = EData()
    doc.query = name
    doc.begin_date = bdate
    doc.end_date = edate
    doc.total_tweets = total
    doc.negative_tweets = neg
    doc.positive_tweets = pos
    doc.neutral_tweets = neut

    doc.save()
    phone = Smartphone.objects(name=name).first()
    phone.extracted_data_ids.append(doc.id)
    phone.save()
