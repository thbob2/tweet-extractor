from json.decoder import JSONDecodeError
import regex as re
import pickle
import json
import pandas as pd
import nltk 
import emoji
from textblob import TextBlob

from textblob.sentiments import NaiveBayesAnalyzer 
from textblob.classifiers import NaiveBayesClassifier
from textblob.blob import Blobber
from textblob.translate import Translator
words = set(nltk.corpus.words.words())
from twitter_client import *
from Matweet import Tweet
from os import error, listdir
from os.path import isfile, join
import os 
import datetime as dt
from exceptionsaver import ExceptionSaver
from googletrans import Translator
import httpx
timout = httpx.Timeout(30)	

class Lexor(object):
    def __init__(self):
        self.companies = os.getcwd()+"/python/corp/data3.0/companies/"
        self.phones = os.getcwd()+"/python/corp/data3.0/smartphones/"
        self.laptops = os.getcwd()+"/python/corp/data3.0/laptops/"
        self.blober = Blobber(analyzer=NaiveBayesAnalyzer())
        self.translator = Translator()

    
    
    def translate(self,text):
        blob = ""
        ok = True
        while(ok):
            try:
                translated = self.translator.translate(text, dest='en')
                blob = translated.text
                ok  = not ok
            except error as e:
                ExceptionSaver().save(str(e))
                continue
        return str(blob)

    def feelingBayes(self,text):
        blob = self.blober(text).sentiment
        return {
            "classisication" : blob[0],
            "positivity" :blob[1],
            "negativity" : blob[2]
        }

    def feeling(self,text):
        result = TextBlob(text)          
        if(result.sentiment[0]>0): 
            return "positive".format(result.sentiment[0])
        elif(result.sentiment[0]==0): 
            return"nutral".format(result.sentiment[0])
        else: 
            return "negative".format(result.sentiment[0])    

    

if __name__ == '__main__':

    lex = Lexor()

    tb = Blobber(analyzer=NaiveBayesAnalyzer())
    print(lex.feelingBayes("ILOVE PIZZA"))
    print(lex.feeling("ILOVE PIZZA"))
    test = lex.translate("j'aime la pizza")
     