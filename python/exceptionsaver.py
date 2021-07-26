import datetime as dt
import json 
from os.path import isfile, join
import os 
import sys
class ExceptionSaver(object):
    
    def __init__(self):
        self.date = dt.datetime.today()
       
    def save(self,exceptionMessage):
        with open(os.getcwd()+"/python/logs/exceptionlogs.txt","a") as logs:
            logs.write(str(exceptionMessage)+":::"+str(self.date)+"\n")