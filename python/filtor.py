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

def filter():
    
    file = open(os.getcwd()+"/python/corp/assets/companies.txt","r")
    lines = file.read().splitlines()
    file.close()
    return lines

if __name__ == '__main__':
    words = filter()
    print(words)
    