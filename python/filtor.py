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

companies = os.getcwd()+"/python/corp/data3.0/companies/"
phones = os.getcwd()+"/python/corp/data3.0/smartphones/"
laptops = os.getcwd()+"/python/corp/data3.0/laptops/"

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
    rpath = os.getcwd()+"/python/corp/data3.0/" + parent
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


#!.########.####.##.......########.########.########...######.
#!.##........##..##..........##....##.......##.....##.##....##
#!.##........##..##..........##....##.......##.....##.##......
#!.######....##..##..........##....######...########...######.
#!.##........##..##..........##....##.......##...##.........##
#!.##........##..##..........##....##.......##....##..##....##
#!.##.......####.########....##....########.##.....##..######.

def filterPhones():
    rpath = os.getcwd()+"/python/corp/data/"
    path = os.getcwd()+"/python/corp/data2.0/smartphones/"
    corp = [f for f in listdir(os.getcwd()+'/python/corp/data/')]
    smartphones = [f for f in listdir(path)]
    classNames = ontologieClasses(os.getcwd()+"/python/corp/assets/smartphone.json")
    stats = {}
    emptyfile=0
    lex = Lexor()
    
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
                                    
                                    tempo.text= clean(tempo.text)
                                    print(tempo.text)
                                    for name in classNames:
                                        #eticting + elaguing
                                        if (re.search(r'\b{}\b'.format(name.lower()),tempo.text) or re.search(r'\b{}\b'.format(name.upper()),tempo.text) or re.search(r'\b{}\b'.format(name),tempo.text)!=None):
                                            tempo.mention.append(name)
                                            
                                        else:
                                            continue
                                    tempo.label= lex.feeling(tempo.text)
                                    print("nb on {}".format(cpt))
                                    cpt+=1
                                    tempo.note = lex.feelingBayes(tempo.text)
                                    tweetArray.append(tempo)
                                #else:
                                #    tempo.translation = lex.translate(tempo.text)
                                #    tempo.translation = clean(tempo.translation)
                                #    for name in classNames:
                                #        #eticting + elaguing
                                #        if (re.search(r'\b{}\b'.format(name.lower()),tempo.translation) or re.search(r'\b{}\b'.format(name.upper()),tempo.translation) or re.search(r'\b{}\b'.format(name),tempo.translation)!=None):
                                #            tempo.mention.append(name)
                                #            
                                #        else:
                                #            continue
                                #    tempo.label = lex.feeling(tempo.translation)
                                #    tempo.note = lex.feelingBayes(tempo.translation)
                                #    tweetArray.append(tempo)    
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
    emptyfile = 0
    lex = Lexor()
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
                                    tempo.note = lex.feelingBayes(tempo.text)
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
    lex = Lexor()
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
                        cpt = 0
                        for tweet in data["tweets"]:                            
                            try:
                                stats[tweet["lang"]]+=1
                            except KeyError as e:
                                try:
                                    stats[tweet["lang"]]=1
                                except KeyError as e:
                                    continue
                            try:
                                tempo = Tweet(tweet["id"],tweet['text'],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"])
                                if tempo.lang=="en":
                                    #cleaning
                                    print(tempo.text)
                                    tempo.text= clean(tempo.text)

                                    tempo.label= lex.feeling(tempo.text)
                                    print("nb on {}".format(cpt))
                                    cpt+=1
                                    tempo.note = lex.feelingBayes(tempo.text)
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
    with open (os.getcwd()+"/python/corp/stats/companies-stats.json","wb") as file:
        string =  json.dumps(towrite,indent=4,ensure_ascii=False).encode("utf8")
        file.write(string)

#*..#######..##....##.########..#######..##........#######...######...##....##
#*.##.....##.###...##....##....##.....##.##.......##.....##.##....##...##..##.
#*.##.....##.####..##....##....##.....##.##.......##.....##.##..........####..
#*.##.....##.##.##.##....##....##.....##.##.......##.....##.##...####....##...
#*.##.....##.##..####....##....##.....##.##.......##.....##.##....##.....##...
#*.##.....##.##...###....##....##.....##.##.......##.....##.##....##.....##...
#*..#######..##....##....##.....#######..########..#######...######......##...
#*..######..##..........###.....######...######..########..######.
#*.##....##.##.........##.##...##....##.##....##.##.......##....##
#*.##.......##........##...##..##.......##.......##.......##......
#*.##.......##.......##.....##..######...######..######....######.
#*.##.......##.......#########.......##.......##.##.............##
#*.##....##.##.......##.....##.##....##.##....##.##.......##....##
#*..######..########.##.....##..######...######..########..######.

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
    
#?.########.##.....##.########..##........#######..####.########.####.##....##..######.....
#?.##........##...##..##.....##.##.......##.....##..##.....##.....##..###...##.##....##....
#?.##.........##.##...##.....##.##.......##.....##..##.....##.....##..####..##.##..........
#?.######......###....########..##.......##.....##..##.....##.....##..##.##.##.##...####...
#?.##.........##.##...##........##.......##.....##..##.....##.....##..##..####.##....##....
#?.##........##...##..##........##.......##.....##..##.....##.....##..##...###.##....##....
#?.########.##.....##.##........########..#######..####....##....####.##....##..######.....
#?.########.....###....########....###.......########.####.##.......########..######.
#?.##.....##...##.##......##......##.##......##........##..##.......##.......##....##
#?.##.....##..##...##.....##.....##...##.....##........##..##.......##.......##......
#?.##.....##.##.....##....##....##.....##....######....##..##.......######....######.
#?.##.....##.#########....##....#########....##........##..##.......##.............##
#?.##.....##.##.....##....##....##.....##....##........##..##.......##.......##....##
#?.########..##.....##....##....##.....##....##.......####.########.########..######.    

def sortfunc(stdate):
    rdate = stdate.split("_")[1][0:10].split("-")
    return dt.datetime(int(rdate[0]),int(rdate[1]),int(rdate[2])).date()

def exploreCorp(path):
    folders = []
    
    for i in os.scandir(path):
        folder = {
            "name": i.name,
            "files": []
        }    
        for j in os.scandir(i):
            folder['files'].append(j.path)
        folder['files'].sort(key=sortfunc,reverse=False)
        folders.append(folder)      
    
    return folders

#!.#######..##.....##.##.....##.##....##.##....##.####.########..######.
#!.##....##.##.....##.##.....##.###...##.##...##...##..##.......##....##
#!.##.......##.....##.##.....##.####..##.##..##....##..##.......##......
#!.##.......#########.##.....##.##.##.##.#####.....##..######....######.
#!.##.......##.....##.##.....##.##..####.##..##....##..##.............##
#!.##....#.##.....##.##.....##.##...###.##...##...##..##.......##....##
#!.#######..##.....##..#######..##....##.##....##.####.########..######.



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
                mySaver.save(str(e)+"continued")
                continue
            for tweet in fdata["tweets"]:
                tempo = Tweet(tweet["id"],tweet['text'],str(tweet["created_at"]),tweet["retweet_count"],tweet["favorite_count"],tweet["lang"],tweet["user_id"],tweet["coordinates"],tweet["geo"],tweet['label'],tweet['note'])   
                chunk_m[tempo.label]+=1
                chunk_m['total'] += 1
                alltweets.append(tempo)
                cpt +=1
        
        chunk_m['start'] = alltweets[0].created_at
        chunk_m['end'] = alltweets[len(alltweets)-1].created_at
        chunk_m['tweets'] = [t.dumps() for t in alltweets]
        chunk_list.append(chunk_m)
    return chunk_list




def chunkyboy(path):
    chinks = exploreCorp(path)
    alterpath = path.replace("data2.0","data3.0")
    
    #! going throught phones
    try:
        for folder in chinks:
            towrite = Semantico(folder['files'],30)
            for w in towrite:
                fname = "{0}-{1}--{2}.json".format(folder['name'],str(w['start'])[0:10],str(w['end'])[0:10])
                writer = open(alterpath+folder['name']+"/"+fname,"wb")
                string=json.dumps(w,indent=4,ensure_ascii=False).encode("utf8")
                writer.write(string)
                writer.close    
    except  JSONDecodeError as e :
        mySaver = Es.ExceptionSaver()
        mySaver.save(str(e)+":::")

#!main method
if __name__ == '__main__':
    filter(os.getcwd()+'/python/corp/assets/laptops.txt',"laptops")
    filter(os.getcwd()+'/python/corp/assets/companies.txt',"companies")
    filter(os.getcwd()+'/python/corp/assets/smartphones.txt',"smartphones")
##
    #filter(os.getcwd()+"/python/corp/assets/smartphones.txt","smartphones")
    #filterPhones()
    #filterLaptops()
    
    #filterCompanies()
    chunkyboy(phones)
    
    #sortfunc("infinx note7-data_2021-01-21.json")
    