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
    
    chunk_list = []
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
    cpt = 0 
    for chunk in mychunks:
        chunk_m = month_j
        for f in chunk:
            fdata = readJson(f)
            
            for tweet in fdata["tweets"]:
                tempo = Tweet(tweet["id"],tweet['text'],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"],tweet['label'])
                print("entering naiv bayes {}".format(cpt))
                tempo.note = feelingBayes(tempo.text)
                chunk_m[tempo.label]+=1
                chunk_m['total'] += 1
                chunk_m['tweets'].append(tempo)
                cpt +=1
        
        chunk_m['start'] = chunk_m['tweets'][0].created_at
        chunk_m['end'] = chunk_m['tweets'][len(chunk_m["tweets"]-1)].created_at
        chunk_list.append(chunk_m)
    return chunk_list




def chunkyboy():
    phonechinks = filtor.exploreCorp(filtor.phones)
    compachinks = filtor.exploreCorp(filtor.companies)
    laptochinks = filtor.exploreCorp(filtor.laptops)        
    
    #! going throught phones
    for folder in phonechinks:
        towrite = Semantico(folder['files'],30)
        for w in towrite:
            with open(phones+folder['name']+"/"+folder['name']+w['start']+".json","wb") as writer:
                writer.write(w,indent=4,ensure_ascii=False).encode("utf8")
    

if __name__ == '__main__':

#    print(filtor.exploreCorp(os.getcwd()+"/python/corp/data2.0/laptops/"))

    chunkyboy()