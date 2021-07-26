from json.decoder import JSONDecodeError
import regex as re
import pickle
import json
import pandas as pd
import nltk 
import emoji

words = set(nltk.corpus.words.words())
from textblob.sentiments import NaiveBayesAnalyzer 
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from twitter_client import *
from Matweet import Tweet
from os import error, listdir
from os.path import isfile, join
import os 
import datetime as dt
import exceptionsaver as Es
import filtor as filtor

companies = os.getcwd()+"/python/corp/data3.0/companies/"
phones = os.getcwd()+"/python/corp/data3.0/smartphones/"
laptops = os.getcwd()+"/python/corp/data3.0/laptops/"


# naive bayes felling analyser 
def feelingBayes(text):
    result = TextBlob(text,analyzer=NaiveBayesAnalyzer())
    return result.sentiment

def readJson(path):
    with open(path,'r') as f:
        return json.loads(f.read())



def chunks(l, n):
    
    return [l[i:i + n] for i in range(0, len(l), n)]

def Semantico(files,n):
    
    
    month_j = {
        "start":"",
        "end":"",
        "total":0,
        "positive": 0,
        "nutral":0,
        "negative":0,
        "tweets" : []

    }
    chunk_m = month_j
    mychunks = chunks(files,n)
    for chunk in mychunks:
        
        for f in chunk:
            fdata = readJson(f)
            
            for tweet in fdata["tweets"]:
                tempo = Tweet(tweet["id"],tweet['text'],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"],tweet['label'])
                chunk_m[tempo.label]+=1
                chunk_m['tweets'].append(tempo)
        
        chunk_m['start'] = chunk_m['tweets'][0].created_at
        chunk_m['start'] = chunk_m['tweets'][len(chunk_m["tweets"]-1)].created_at

        print(chunk_m)
        break

if __name__ == '__main__':

    print(filtor.exploreCorp(os.getcwd()+"/python/corp/data2.0/laptops/"))