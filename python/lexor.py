from json.decoder import JSONDecodeError
import regex as re
import pickle
import json
import pandas as pd
import nltk 
import emoji
from textblob import TextBlob
from textblob.blob import Blobber
from textblob.sentiments import NaiveBayesAnalyzer 
from textblob.classifiers import NaiveBayesClassifier
words = set(nltk.corpus.words.words())
from twitter_client import *
from Matweet import Tweet
from os import error, listdir
from os.path import isfile, join
import os 
import datetime as dt
import exceptionsaver as Es
import filtor as filtor

class Lexor(object):
    def __init__(self, *args):
        self.companies = os.getcwd()+"/python/corp/data3.0/companies/"
        self.phones = os.getcwd()+"/python/corp/data3.0/smartphones/"
        self.laptops = os.getcwd()+"/python/corp/data3.0/laptops/"
        self.blober = Blobber(analyzer=NaiveBayesAnalyzer)

    # naive bayes felling analyser 
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

    @classmethod
    def readJson(cls,path):
        with open(path,'r',encoding="utf8") as f:
            return json.loads(f.read())


    @classmethod
    def chunks(cls,l, n):
        
        return [l[i:i + n] for i in range(0, len(l), n)]
    
    @classmethod
    def Semantico(cls,files,n):
        
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
        mychunks = cls.chunks(files,n)
        cpt = 0 

        for chunk in mychunks:
            alltweets = []
            chunk_m = month_j
            for f in chunk:
                try:  
                    fdata = cls.readJson(f)
                except  JSONDecodeError as e :
                    mySaver = Es.ExceptionSaver()
                    mySaver.save(str(e)+"continued")
                    continue
                for tweet in fdata["tweets"]:
                    tempo = Tweet(tweet["id"],tweet['text'],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"],tweet['label'])
                    print("entering naiv bayes {}".format(cpt))
                    tempo.note = cls.feelingBayes(tempo.text)
                    chunk_m[tempo.label]+=1
                    chunk_m['total'] += 1
                    alltweets.append(tempo)
                    cpt +=1
            
            chunk_m['start'] = alltweets[0].created_at
            chunk_m['end'] = alltweets[len(alltweets)-1].created_at
            chunk_m['tweets'] = [t.dumps() for t in alltweets]
            chunk_list.append(chunk_m)
        return chunk_list




    def chunkyboy(self,path):
        chinks = filtor.exploreCorp(path)
        alterpath = path.replace("data2.0","data3.0")
        
        #! going throught phones
        try:
            for folder in chinks:
                towrite = self.Semantico(folder['files'],30)
                for w in towrite:
                    fname = "{0}-{1}--{2}.json".format(folder['name'],str(w['start'])[0:10],str(w['end'])[0:10])
                    writer = open(alterpath+folder['name']+"/"+fname,"wb")
                    string=json.dumps(w,indent=4,ensure_ascii=False).encode("utf8")
                    writer.write(string)
                    writer.close    
        except  JSONDecodeError as e :
            mySaver = Es.ExceptionSaver()
            mySaver.save(str(e)+":::")

if __name__ == '__main__':

#    print(filtor.exploreCorp(os.getcwd()+"/python/corp/data2.0/laptops/"))
    #filtor.filter(os.getcwd()+'/python/corp/assets/smartphones.txt',os.getcwd()+"/python/corp/data3.0/smartphones/")
    #filtor.filter(os.getcwd()+'/python/corp/assets/companies.txt',os.getcwd()+"/python/corp/data3.0/companies/")
    #filtor.filter(os.getcwd()+'/python/corp/assets/laptops.txt',os.getcwd()+"/python/corp/data3.0/laptops/")
    lex = Lexor()
    lex.chunkyboy(filtor.phones)
    lex.chunkyboy(filtor.companies)
    lex.chunkyboy(filtor.laptops)