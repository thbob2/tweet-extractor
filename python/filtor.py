from json.decoder import JSONDecodeError
from nltk import text
import regex as re
import pickle
import json
import pandas as pd
import nltk 
import emoji
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer 
from textblob.classifiers import NaiveBayesClassifier
from textblob import Blobber
from twitter_client import *
from Matweet import Tweet
from os import error, listdir
from os.path import isfile, join
import os 
import datetime as dt
import exceptionsaver as Es
from lexor import Lexor
words = set(nltk.corpus.words.words())

companies = os.getcwd()+"/python/corp/data2.0/companies/"
phones = os.getcwd()+"/python/corp/data2.0/smartphones/"
laptops = os.getcwd()+"/python/corp/data2.0/laptops/"

def clean(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI) #Remove Emojis
    tweet = tweet.replace("#", "").replace("_", " ") #Remove hashtag sign but keep the text
    tweet = " ".join(w for w in nltk.wordpunct_tokenize(tweet) \
        if w.lower() in words or not w.isalpha())
    return tweet

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
        except OSError as e:
            mySaver = Es.ExceptionSaver()
            mySaver.save(str(e))
            
        finally:
            print("going to the next file")

def groupor():
    rpath = os.getcwd()+"/python/corp/data/"
    cpath = os.getcwd()+"/python/corp/data2.0/companies/"
    spath = os.getcwd()+"/python/corp/data2.0/smartphones/"
    lpath = os.getcwd()+"/python/corp/data2.0/laptops/"
    corp = [f for f in listdir(os.getcwd()+'/python/corp/data/')]
    companies = [f for f in listdir(cpath)]
    smartphones = [f for f in listdir(spath)]
    laptops = [f for f in listdir(lpath)]
    emptyfile=0
    for c in corp :
        try:
            tweetArray = []
            entity = c.split("-")[0]
            if entity in companies:
                with open(cpath+entity+"/"+c,"wb") as w:
                    with open(rpath+c,"r",encoding="utf-8") as read:
                        try:
                            data = json.load(read)
                        except JSONDecodeError as e:
                            mySaver = Es.ExceptionSaver()
                            mySaver.save(str(e))
                            print(c +" is the one causing error")
                    if data["tweets"] == []:
                        print("empty array skiped")
                        emptyfile+=1
                        continue
                    else:    
                        for tweet in data["tweets"]:
                            try:
                                tempo = Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                tweetArray.append(tempo)
                            except KeyError as e :
                                mySaver = Es.ExceptionSaver()
                                mySaver.save(str(e))
                                continue   
                        w.write(json.dumps({'tweets':[o.dump() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))


            elif entity in smartphones:
                with open(spath+entity+"/"+c,"wb") as w:
                    with open(rpath+c,"r",encoding="utf-8") as read:
                        try:
                            data = json.load(read)
                        except JSONDecodeError as e:
                            print(c +" is the one causing error")
                            mySaver = Es.ExceptionSaver()
                            mySaver.save(str(e))
                
                    if data["tweets"] == []:
                        print("empty array skiped")
                        emptyfile+=1
                        continue
                    else: 
                        for tweet in data["tweets"]:
                            try:
                                tempo = Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                tweetArray.append(tempo)
                            except KeyError as e :
                                mySaver = Es.ExceptionSaver()
                                mySaver.save(str(e))
                                continue
                        w.write(json.dumps({'tweets':[o.dump() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))
            
            elif entity in laptops:
                with open(lpath+entity+"/"+c,"wb") as w:
                    with open(rpath+c,"r",encoding="utf-8") as read:
                        try:
                            data = json.load(read)
                        except JSONDecodeError as e:
                            mySaver = Es.ExceptionSaver()
                            mySaver.save(str(e)+":::"+c+" is the one causing error")
                            
                    if data["tweets"] == []:
                        
                        emptyfile+=1
                        continue
                    else: 
                        for tweet in data["tweets"]:
                            try:
                                tempo = Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                tweetArray.append(tempo)
                            except KeyError as e :
                                mySaver = Es.ExceptionSaver()
                                mySaver.save(str(e))
                                continue
                        w.write(json.dumps({'tweets':[o.dump() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))
        except ValueError as e:
            mySaver = Es.ExceptionSaver()
            mySaver.save(str(e))
            continue
    print("number of empty files = "+str(emptyfile))



def filterPhones():
    rpath = os.getcwd()+"/python/corp/data/"
    path = os.getcwd()+"/python/corp/data2.0/smartphones/"
    corp = [f for f in listdir(os.getcwd()+'/python/corp/data/')]
    smartphones = [f for f in listdir(path)]
    classNames = ontologieClasses(os.getcwd()+"/python/corp/assets/smartphone.json")
    stats = {}
    emptyfile=0
    lex = Lexor()
    tb = Blobber(analyzer=NaiveBayesAnalyzer())
    for c in corp :
        try:
            tweetArray = []
            entity = c.split("-")[0]
            if entity in smartphones:              
                with open(rpath+c,"r",encoding="utf-8") as read:
                    try:
                        data = json.load(read)
                    except JSONDecodeError as e:
                        print(c +" is the one causing error")
                    if data["tweets"] != []:                                        
                        cpt = 0
                        for tweet in data["tweets"]:                            
                            try:
                                stats[tweet["lang"]]+=1
                            except KeyError as e:
                                stats[tweet["lang"]]=1
                            try:
                                tempo = Tweet(tweet["id"],tweet['text'],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                if tempo.lang=="en":
                                    #cleaning
                                    print(tempo.text)
                                    tempo.text= clean(tempo.text)
                                    for name in classNames:
                                        #eticting + elaguing
                                        if (re.search(r'\b{}\b'.format(name.lower()),tempo.text) or re.search(r'\b{}\b'.format(name.upper()),tempo.text) or re.search(r'\b{}\b'.format(name),tempo.text)!=None):
                                            tempo.mention.append(name)
                                            
                                        else:
                                            continue
                                    tempo.label= lex.feeling(tempo.text)
                                    print("nb on {}".format(cpt))
                                    cpt+=1
                                    tempo.note = lex.feelingBayes(tempo.text,tb)
                                    tweetArray.append(tempo)
                                
                            except KeyError as e :
                                continue
                        if len(tweetArray) > 0:
                            with open(path+entity+"/"+c,"wb") as w: 
                                w.write(json.dumps({'tweets':[o.dumps() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))
                    elif data["tweets"]==[]:
                    
                        emptyfile+=1
                        continue   
                
        except ValueError as e:
            mySaver = Es.ExceptionSaver()
            mySaver.save(str(e))
            continue
    towrite = {
        "empty-files" : emptyfile,
        "languages-stats": stats
    }
    with open (os.getcwd()+"/python/corp/stats/phones-stats.json","wb") as file:
        string =  json.dumps(towrite,indent=4,ensure_ascii=False).encode("utf8")
        file.write(string)
    
def filterLaptops():
    rpath = os.getcwd()+"/python/corp/data/"
    path = os.getcwd()+"/python/corp/data2.0/laptops/"
    corp = [f for f in listdir(os.getcwd()+'/python/corp/data/')]
    laptops = [f for f in listdir(path)]
    classNames = ontologieClasses(os.getcwd()+"/python/corp/assets/laptop.json")
    stats = {}
    emptyfile=0
    for c in corp :
        try:
            tweetArray = []
            entity = c.split("-")[0]
            if entity in laptops:
                
                with open(rpath+c,"r",encoding="utf-8") as read:
                    try:
                        data = json.load(read)
                    except JSONDecodeError as e:
                        print(c +" is the one causing error")
                    if data["tweets"] != []:
                        with open(path+entity+"/"+c,"wb") as w:                  
                            cpt =1
                            for tweet in data["tweets"]:
                                
                                try:
                                    stats[tweet["lang"]]+=1
                                except KeyError as e:
                                    stats[tweet["lang"]]=1
                                try:
                                    text=cleaner(tweet["text"])
                                    tempo = Tweet(tweet["id"],text,str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                    if tempo.lang == "en":
                                        for name in classNames:
                                            #eticting + elaguing
                                            if (re.search(r'\b{}\b'.format(name.lower()),tweet["text"]) or re.search(r'\b{}\b'.format(name.upper()),tweet["text"]) or re.search(r'\b{}\b'.format(name),tweet["text"])!=None):
                                                tempo.mention.append(name)
                                        tempo.label = feeling(tempo.text)
                                        print("nb on laps {}".format(cpt))
                                        tempo.note = feelingBayes(tempo.text)
                                        tweetArray.append(tempo)
                                        cpt+=1

                                except KeyError as e :
                                    continue
                            if len(tweetArray) > 0:
                                w.write(json.dumps({'tweets':[o.dumps() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))
                    elif data["tweets"]==[]:
                        
                        emptyfile+=1
                        continue   
                
        except ValueError as e:
            mySaver = Es.ExceptionSaver()
            mySaver.save(str(e))
            continue
            
    towrite = {
        "empty-files" : emptyfile,
        "languages-stats": stats
    }
    with open (os.getcwd()+"/python/corp/stats/laptops-stats.json","wb") as file:
        string =  json.dumps(towrite,indent=4,ensure_ascii=False).encode("utf8")
        file.write(string)

def filterCompanies():
    rpath = os.getcwd()+"/python/corp/data/"
    path = os.getcwd()+"/python/corp/data2.0/companies/"
    corp = [f for f in listdir(os.getcwd()+'/python/corp/data/')]
    companies = [f for f in listdir(path)]
    stats = {}
    emptyfile=0
    for c in corp :
        try:
            tweetArray = []
            entity = c.split("-")[0]
            if entity in companies:
                with open(rpath+c,"r",encoding="utf-8") as read:
                    try:
                        data = json.load(read)
                    except JSONDecodeError as e:
                        print(c +" is the one causing error")
                    if data["tweets"] != []:
                        with open(path+entity+"/"+c,"wb") as w:                  
                            cpt =0
                            for tweet in data["tweets"]:
                                
                                try:
                                    stats[tweet["lang"]]+=1
                                except KeyError as e:
                                    try:
                                        stats[tweet["lang"]]=1
                                    except:
                                        continue
                                try:
                                    text=cleaner(tweet["text"])
                                    tempo = Tweet(tweet["id"],text,str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                    if tempo.lang =="en":
                                        tempo.label = feeling(tempo.text)
                                        print("nb on companies {}".format(cpt))
                                        tempo.note = feelingBayes(tempo.text)                        
                                        tweetArray.append(tempo)
                                        cpt +=1

                                except KeyError as e :
                                    continue
                            if len(tweetArray) > 0:
                                w.write(json.dumps({'tweets':[o.dumps() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))
                    elif data["tweets"]==[]:
                        
                        emptyfile+=1
                        continue   
                
        except ValueError as e:
            mySaver = Es.ExceptionSaver()
            mySaver.save(str(e))
            continue
    towrite = {
        "empty-files" : emptyfile,
        "languages-stats": stats
    }
    with open (os.getcwd()+"/python/corp/stats/companies-stats.json","wb") as file:
        string =  json.dumps(towrite,indent=4,ensure_ascii=False).encode("utf8")
        file.write(string)

def getChilds(obj):
    res = []
    res.append(obj["name"])
    for c in obj["childs"]:
        res.extend(getChilds(c))

    return res
        

#! methods that returns the ontologies subclasses
def ontologieClasses(onto):
    clsList = {}
    res = []
    with open(onto,"r") as file:
        try:
            clsList = json.load(file)
            p = clsList['product']
            res = getChilds(p[0])
        except JSONDecodeError as e:
            mySaver = Es.ExceptionSaver()
            mySaver.save(str(e))
    return (res)
    
def exploreCorp(path):
    folders = []
    
    for i in os.scandir(path):
        folder = {
            "name": i.name,
            "files": []
        }    
        for j in os.scandir(i):
            folder['files'].append(j.path)
        folders.append(folder)      
    return folders

#!main method
if __name__ == '__main__':
    #filter(os.getcwd()+'/python/corp/assets/laptops.txt',"laptops")
    #filter(os.getcwd()+'/python/corp/assets/companies.txt',"companies")
    filter(os.getcwd()+'/python/corp/assets/smartphones.txt',"smartphones")
##
    #filter(os.getcwd()+"/python/corp/assets/smartphones.txt","smartphones")
    filterPhones()
    #filterLaptops()
    #
    #filterCompanies()
    
    #sphones = os.getcwd()+"/python/corp/assets/smartphone.json"
    #ontologieClasses(sphones)
    folders = exploreCorp(phones)
    with open(os.getcwd()+"/python/logs/test.txt","w") as w:
        w.write(str(folders))