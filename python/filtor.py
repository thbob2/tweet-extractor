import regex as re
import pickle
import json
import pandas as pd
from textblob import TextBlob
from twitter_client import *
from Matweet import Tweet
from os import listdir
from os.path import isfile, join
import os 
import datetime as dt

def filter(path,parent):
    rpath = os.getcwd()+"/python/corp/data2.0/" + parent
    try:
        os.mkdir(rpath)
    except OSError as e:
        print('parent exist')
    file = open(path,"r")
    dirs = file.read().splitlines()
    file.close()
    for d in dirs:
        try:
            os.mkdir(os.path.join(rpath,d))
        except OSError as error:
            print("file already exist skipping ahead")
        finally:
            print("going to the next file")


if __name__ == '__main__':
    #filter(os.getcwd()+'/python/corp/assets/laptops.txt','laptops')
    
    