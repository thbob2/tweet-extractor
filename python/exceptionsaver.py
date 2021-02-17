import datetime as dt
import json 
from os.path import isfile, join
import os 
import sys
class ExceptionSaver(object):
    
    def __init__(self):
       exmap = []
    def save(self,e):
        exmap.add(e)


"""if __name__ == '__main__':
    
    try:
        print(5/0)
    except Exception as e:
        print(e)
    finally: 
        print("gg boss")"""