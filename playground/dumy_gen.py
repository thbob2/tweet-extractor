import datetime as dt
import json
import os


dumy_dir1 = os.getcwd()+"/python/corp/data2.0/laptops/MACBOOK PRO"

dirs = os.listdir(dumy_dir1) 

for d in dirs:
    data = readJson(d) 
