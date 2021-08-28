import json
import os
import data.mongo_setup as mongo_setup
from data.smartphones import SDiscription
from data.laptops import LDiscription
from filtor import exploreCorp,readJson
from services.data_service import *
from colorama import Fore

companies = os.getcwd()+"/python/corp/data3.0/companies/"
smartphones = os.getcwd()+"/python/corp/data3.0/smartphones/"
laptops = os.getcwd()+"/python/corp/data3.0/laptops/"

def init():
    mongo_setup.global_init()
"""
?.?########..##.....##..#######..##....##.########..######.
?.?##.....##.##.....##.##.....##.###...##.##.......##....##
?.?##.....##.##.....##.##.....##.####..##.##.......##......
?.?########..#########.##.....##.##.##.##.######....######.
?.?##........##.....##.##.....##.##..####.##.............##
?.?##........##.....##.##.....##.##...###.##.......##....##
?.?##........##.....##..#######..##....##.########..######.
"""
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

    success_msg('smartphones imported')



def import_phone_data():
    data = exploreCorp(smartphones)
    for d in data:
        for file in d['files']:
            with open(file,"r") as read:
                load = readJson(file)
                name = load['query']
                add_phone_data(d['name'],load['start'],load['end'],load['total'],load['positive'],load['negative'],
                load['neutral'],load['tweets']
                )

    success_msg('phone data tweets imported successfully')
"""
!##..........###....########..########..#######..########...######.
!##.........##.##...##.....##....##....##.....##.##.....##.##....##
!##........##...##..##.....##....##....##.....##.##.....##.##......
!##.......##.....##.########.....##....##.....##.########...######.
!##.......#########.##...........##....##.....##.##..............##
!##.......##.....##.##...........##....##.....##.##........##....##
!########.##.....##.##...........##.....#######..##.........######.
"""
def import_laptops():
    
    with open(os.getcwd()+"/python/corp/assets/laptops.json","r") as read:
        laptops = json.load(read)
        for laptop in laptops['laptops']:
            dic = laptop['description']
            desc = LDiscription()
            desc.network = dic['network']
            desc.body = dic['body']
            desc.os = dic['os']
            desc.cpu = dic['cpu']
            desc.gpu = dic['gpu']
            desc.ram = dic['ram']
            desc.webcam = dic['webcam']
            desc.battery = dic['battery']
            create_laptop(laptop['model-name'],laptop['manifactor'],laptop['date-of-release'],desc)

    success_msg('laptops imported')

def import_laptops_data():
    data = exploreCorp(laptops)
    for d in data:
        for file in d['files']:
            load = readJson(file)
            add_laptops_data(d['name'],load['start'],load['end'],load['total'],load['positive'],load['negative'],
            load['neutral'],load['tweets']
            )

    success_msg('laptops data tweets imported successfully')   

"""
TODO..######...#######..##.....##.########.....###....##....##.####.########..######.
TODO.##....##.##.....##.###...###.##.....##...##.##...###...##..##..##.......##....##
TODO.##.......##.....##.####.####.##.....##..##...##..####..##..##..##.......##......
TODO.##.......##.....##.##.###.##.########..##.....##.##.##.##..##..######....######.
TODO.##.......##.....##.##.....##.##........#########.##..####..##..##.............##
TODO.##....##.##.....##.##.....##.##........##.....##.##...###..##..##.......##....##
TODO..######...#######..##.....##.##........##.....##.##....##.####.########..######.
"""


def import_companies():
    pass

def impro_companies_data():
    pass

"""
!.##.....##.########.####.##.......####.########.####.########..######.
!.##.....##....##.....##..##........##.....##.....##..##.......##....##
!.##.....##....##.....##..##........##.....##.....##..##.......##......
!.##.....##....##.....##..##........##.....##.....##..######....######.
!.##.....##....##.....##..##........##.....##.....##..##.............##
!.##.....##....##.....##..##........##.....##.....##..##.......##....##
!..#######.....##....####.########.####....##....####.########..######.
"""

def success_msg(text):
    print(Fore.LIGHTGREEN_EX + text + Fore.WHITE)


def error_msg(text):
    print(Fore.LIGHTRED_EX + text + Fore.WHITE)


if __name__ == '__main__':
    #init()
    #import_laptops()
    #import_laptops_data()