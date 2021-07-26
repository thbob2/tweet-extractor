from json.decoder import JSONDecodeError
import regex as re
import pickle
import json
import pandas as pd
import nltk 
import emoji
import platform

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
    with open(path,'r',encoding="utf8") as f:
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
        alltweets = []
        chunk_m = month_j
        for f in chunk:
            try:  
                fdata = readJson(f)
            except  JSONDecodeError as e :
                mySaver = Es.ExceptionSaver()
                mySaver.save(str(e)+":::")
                continue
            for tweet in fdata["tweets"]:
                tempo = Tweet(tweet["id"],tweet['text'],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"],tweet['label'])
                print("entering naiv bayes {}".format(cpt))
                #tempo.note = feelingBayes(tempo.text)
                chunk_m[tempo.label]+=1
                chunk_m['total'] += 1
                alltweets.append(tempo)
                cpt +=1
        
        chunk_m['start'] = alltweets[0].created_at
        chunk_m['end'] = alltweets[len(alltweets)-1].created_at
        chunk_m['tweets'] = [t.dumps() for t in alltweets]
        chunk_list.append(chunk_m)
    return chunk_list




def chunkyboy():
    phonechinks = filtor.exploreCorp(filtor.phones)
    compachinks = filtor.exploreCorp(filtor.companies)
    laptochinks = filtor.exploreCorp(filtor.laptops)        
    
    #! going throught phones
    try:
        for folder in phonechinks:
            towrite = Semantico(folder['files'],30)
            for w in towrite:
                if(platform.system() == "windows"):
                    with open(str(phones+folder['name']+"/"+folder['name']+w['start']+".json").replace("/","\\"),"wb") as writer:
                        writer.write(w,indent=4,ensure_ascii=False).encode("utf8")
                else:    
                    with open(phones+folder['name']+"/"+folder['name']+w['start']+".json","wb") as writer:
                        string=json.dumps(w,indent=4,ensure_ascii=False).encode("utf8")
                        writer.write(string)
    except  JSONDecodeError as e :
        mySaver = Es.ExceptionSaver()
        mySaver.save(str(e)+":::")

if __name__ == '__main__':

#    print(filtor.exploreCorp(os.getcwd()+"/python/corp/data2.0/laptops/"))
    filtor.filter(os.getcwd()+'/python/corp/assets/smartphones.txt',phones)
    filtor.filter(os.getcwd()+'/python/corp/assets/companies.txt',companies)
    filtor.filter(os.getcwd()+'/python/corp/assets/laptops.txt',laptops)
    chunkyboy()