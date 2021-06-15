from json.decoder import JSONDecodeError
import regex as re
import pickle
import json
import pandas as pd
from textblob import TextBlob
from twitter_client import *
from Matweet import Tweet
from os import error, listdir
from os.path import isfile, join
import os 
import datetime as dt
from googletrans import Translator

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
                                continue    
                        w.write(json.dumps({'tweets':[o.dump() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))


            elif entity in smartphones:
                with open(spath+entity+"/"+c,"wb") as w:
                    with open(rpath+c,"r",encoding="utf-8") as read:
                        try:
                            data = json.load(read)
                        except JSONDecodeError as e:
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
                                continue 
                        w.write(json.dumps({'tweets':[o.dump() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))
            
            elif entity in laptops:
                with open(lpath+entity+"/"+c,"wb") as w:
                    with open(rpath+c,"r",encoding="utf-8") as read:
                        try:
                            data = json.load(read)
                        except JSONDecodeError as e:
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
                                continue 
                        w.write(json.dumps({'tweets':[o.dump() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))
        except ValueError as e:
            print(e)
            continue
    print("number of empty files = "+str(emptyfile))

#0categorizing

def filterPhones():
    rpath = os.getcwd()+"/python/corp/data/"
    path = os.getcwd()+"/python/corp/data2.0/test/"
    corp = [f for f in listdir(os.getcwd()+'/python/corp/data/')]
    smartphones = [f for f in listdir(path)]
    classNames = ontologieClasses(os.getcwd()+"/python/corp/assets/smartphone.json")
    stats = {}
    emptyfile=0
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
                        with open(path+entity+"/"+c,"wb") as w:                  
                            for tweet in data["tweets"]:
                                try:
                                    stats[tweet["lang"]]+=1
                                except KeyError as e:
                                    stats[tweet["lang"]]=1
                                try:
                                    if tweet["lang"]=="en":
                                        for name in classNames:
                                            if (re.search(r'\b{}\b'.format(name.lower()),tweet["text"]) or re.search(r'\b{}\b'.format(name.upper()),tweet["text"]) or re.search(r'\b{}\b'.format(name),tweet["text"])!=None):
                                                tempo = Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                                tweetArray.append(tempo)
                                            else:
                                                continue                         
                                except KeyError as e :
                                    continue
                    elif data["tweets"]==[]:
                        print("empty array skiped")
                        emptyfile+=1
                        continue   
                if tweetArray != []:
                    w.write(json.dumps({'tweets':[o.dump() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))
        except ValueError as e:
            print(e)
            continue
    towrite = {
        "empty-files" : emptyfile,
        "languages-stats": stats
    }
    with open (os.getcwd()+"/python/corp/stats/test-stats.json","wb") as file:
        string =  json.dumps(towrite,indent=4,ensure_ascii=False).encode("utf8")
        file.write(string)
    
def filterLaptops():
    rpath = os.getcwd()+"/python/corp/data/"
    path = os.getcwd()+"/python/corp/data2.0/laptops/"
    corp = [f for f in listdir(os.getcwd()+'/python/corp/data/')]
    laptops = [f for f in listdir(path)]
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
                            for tweet in data["tweets"]:
                                try:
                                    stats[tweet["lang"]]+=1
                                except KeyError as e:
                                    stats[tweet["lang"]]=1
                                try:
                                    if tweet["lang"]=="en":
                                        tempo = Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                        tweetArray.append(tempo)
                                    else:
                                        continue

                                except KeyError as e :
                                    continue
                    elif data["teeets"] == [] :
                        print("empty array skiped")
                        emptyfile+=1
                        continue
            w.write(json.dumps({'tweets':[o.dump() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))

                        
        except ValueError as e:
            print(e)
            continue
    print("number of empty files = "+str(emptyfile))
    print(stats)
    
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
                with open(path+entity+"/"+c,"wb") as w:
                    with open(rpath+c,"r",encoding="utf-8") as read:
                        try:
                            data = json.load(read)
                        except JSONDecodeError as e:
                            print(c +" is the one causing error")
                    if data["tweets"] == []:
                        print("empty array skiped")
                        emptyfile+=1
                        continue
                    else: 
                        for tweet in data["tweets"]:
                            
                            try:
                                stats[tweet["lang"]]+=1
                            except KeyError as e:
                                try:
                                    stats[tweet["lang"]]=1
                                except KeyError as e:
                                    pass
                            try:
                                if tweet["lang"]=="en":
                                    tempo = Tweet(tweet["id"],tweet["text"],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                    tweetArray.append(tempo)
                                else:
                                    continue
                            
                            except KeyError as e :
                                continue
                            
                            
                        w.write(json.dumps({'tweets':[o.dump() for o in tweetArray]},indent=4,ensure_ascii=False).encode("utf8"))
        except ValueError as e:
            print(e)
            continue
    print("number of empty files = "+str(emptyfile))
    print(stats)

def getChilds(obj):
    res = []
    res.append(obj["name"])
    for c in obj["childs"]:
        res.extend(getChilds(c))

    return res
        
    
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
            print( "causing error")
    return (res)
    

    
#!main method
if __name__ == '__main__':
    #filter(os.getcwd()+'/python/corp/assets/laptops.txt','laptops')
    #filter(os.getcwd()+'/python/corp/assets/companies.txt','companies')
    #filter(os.getcwd()+'/python/corp/assets/smartphones.txt','smartphones')
#
    #groupor()
    #filterLaptops()
    #filterCompanies()
    filterPhones()
    #sphones = os.getcwd()+"/python/corp/assets/smartphone.json"
    #ontologieClasses(sphones)