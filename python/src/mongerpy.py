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
        for phone in phones['smartphones']:
            dic = phone['description']
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



def import_phones_data():
    data = exploreCorp(smartphones,False)
    for d in data:
        for file in d['files']:
            load = readJson(file)
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
    data = exploreCorp(laptops,False)
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
    with open(os.getcwd()+"/python/corp/assets//companies.json","r") as read:
        companies = json.load(read)
        for company in companies['companies']:
            create_company(company['name'],company["owner"],company['product-category'],company['net-worth'])
            

    success_msg('companies imported')

def improt_companies_data():
    data = exploreCorp(companies,False)
    for d in data:
        for file in d['files']:
            load = readJson(file)
            add_companies_data(d['name'],load['start'],load['end'],load['total'],load['positive'],load['negative'],
            load['neutral'],load['tweets']
            )
    success_msg("Companies tweets Data imported successfully")


def export_database(dbname,collection):
    command = "mongoexport --db {0} -c {1} --out data/{1}.json".format(dbname,collection)
    os.system(command)
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
    init()
    import_phones()
    import_phones_data()
    import_laptops()
    import_laptops_data()
    import_companies()
    improt_companies_data()

    #export_database("t_punch","companies")
    #export_database("t_punch","laptops")
    #export_database("t_punch","smartphones")
    #export_database("t_punch","extracted_data")
    #export_database("t_punch","tweets")