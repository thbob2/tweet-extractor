import json
import os
import data.mongo_setup as mongo_setup
from data.smartphones import SDiscription
from data.laptops import LDiscription
import services.data_service as svc
from filtor import exploreCorp,readJson
from services.data_service import create_smartphone
from services.data_service import add_phone_data, find_phone_by_name

companies = os.getcwd()+"/python/corp/data3.0/companies/"
smartphones = os.getcwd()+"/python/corp/data3.0/smartphones/"
laptops = os.getcwd()+"/python/corp/data3.0/laptops/"

def init():
    mongo_setup.global_init()

def import_phones():

    with open(os.getcwd()+"/python/corp/assets/smartphones.json","r") as read:
        phones = json.load(read)
        for phone in phones['models']:
            dic = phone['discription']
            desc = SDiscription()
            desc.network = dic['network']
            desc.body = dic['body']
            desc.os = dic['os']
            desc.cpu = dic['cpu']
            desc.gpu = dic['gpu']
            desc.memory = dic['memory']
            desc.main_camera = dic['main-camera']
            desc.selfie_camera = dic['selfie-camera']
            desc.battery = dic['battery']
            create_smartphone(phone['model-name'],phone['manifactor'],phone['date-of-release'],desc)

    print('import ended')

def import_phone_data():
    data = exploreCorp(smartphones)
    for d in data:
        for file in d['files']:
            with open(file,"r") as read:
                load = readJson(file)
                name = load['query']
                add_phone_data(d['name'],load['start'],load['end'],load['total'],load['positive'],load['negative'],
                load['nutral'],load['tweets']
                )

    print('phone data tweets imported successfully')

if __name__ == '__main__':
    init()
    import_phones()
    import_phone_data()