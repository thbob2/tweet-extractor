import json
import os
import data.mongo_setup as mongo_setup
from data.smartphones import SDiscription
from data.laptops import LDiscription
import services.data_service as svc
from filtor import exploreCorp
from services.data_service import create_smartphone

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

if __name__ == '__main__':
    init()
    import_phones()