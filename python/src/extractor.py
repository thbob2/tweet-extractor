from json.decoder import JSONDecodeError
import regex as re
import time
import pickle
import tweepy
import json
import pandas as pd
from textblob import TextBlob
from twitter_client import *
from Matweet import Tweet
from os import listdir
from os.path import isfile, join
import os 
import datetime as dt
import exceptionsaver as Es
class Extractor(object):
    def MainCorpExtraction(self,api,since,until,query):
        print('it started hello world')
        start = since.strftime('%Y-%m-%d')
        end = until.strftime('%Y-%m-%d')
        dayDate = (until - dt.timedelta(days=1)).strftime('%Y-%m-%d')
        backoffCounter  = 1 
        #while True :
        #    try:
        print(query)
        Alltweets=tweepy.Cursor(api.search,q=query,wait_on_rate_limit=True, wait_on_rate_limit_notify=True,since=start,until=end,count=200).pages(100)

        cpt=1
        Tweets=[]
        while True:
            try:
                for page in Alltweets:
                    for tweet in page:
                        tempo = Tweet(tweet.id,tweet.text,str(tweet.created_at),tweet.retweet_count,tweet.favorite_count,tweet.lang,tweet.user.id,tweet.coordinates,tweet.geo)      
                        print(" tweet fetched {} downloaded,time: {}".format(cpt,str(tempo.created_at))) # on la garde pour l'instant
                        lastDate=str(tempo.created_at)[:10]
                        if(lastDate!=dayDate):
                            newf = os.getcwd()+"/python/corp/data/"+str(query).strip()+"-data_{}.json".format(dayDate)
                            with open(newf,"wb") as file2:
                                string=json.dumps({'tweets':[o.dumps() for o in Tweets]},indent=4,ensure_ascii=False).encode("utf8")
                                file2.write(string)
                                Tweets = []
                                dayDate=lastDate
                        Tweets.append(tempo)
                        cpt+=1
                break
                #break
                #    except tweepy.TweepError as e:
                #        print(e.reason)
                #        time.sleep(60 * backoffCounter)
                #        backoffCounter += 1
                #        continue
            except tweepy.error.TweepError as e:
                mySaver = Es.ExceptionSaver()
                mySaver.save(str(e))
                continue

if __name__ == '__main__':

    with open(os.getcwd()+"/user.json","r") as ufile:
        try:
            data = json.load(ufile)
        except JSONDecodeError as e:
            print(" is the one causing error")
            
    user = data["user"]
    agent = TwitterAgent(user["key"],user["secret_key"],user["access_token"],user["access_token_secret"])
    api = agent.get_twitter_client()
    ext = Extractor()
    until = dt.datetime.today()
    since = until - dt.timedelta(days=7)
    print('outside the call')
    lappath = open(os.getcwd()+"/python/corp/assets/laptops.txt","r") 
    for q in lappath:
        ext.MainCorpExtraction(api,since,dt.datetime.today(),q)
##
    spath = open(os.getcwd()+"/python/corp/assets/companies.txt","r")
# ####
    for query in spath:
        ext.MainCorpExtraction(api,since,dt.datetime.today(),query)
###
    smart = open(os.getcwd()+"/python/corp/assets/smartphones.txt","r") 
    for q in smart:
       ext.MainCorpExtraction(api,since,dt.datetime.today(),q)
    print('end of the call')
#                                    