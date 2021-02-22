import regex as re
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
class Extractor(object):
    def MainCorpExtraction(self,api,since,until,query):
        print('it started hello world')
        start = since.strftime('%Y-%m-%d')
        end = until.strftime('%Y-%m-%d')
        dayDate = (until - dt.timedelta(days=1)).strftime('%Y-%m-%d')
        
        Alltweets=tweepy.Cursor(api.search,q=query,wait_on_rate_limit=True, wait_on_rate_limit_notify=True,since=start,until=end,count=200).pages()

        cpt=1
        Tweets=[]
        for page in Alltweets:
            for tweet in page:
                tempo = Tweet(tweet.id,tweet.text,str(tweet.created_at),tweet.retweet_count,tweet.favorite_count,tweet.lang,tweet.user.id,tweet.coordinates,tweet.geo)      
                print("Tweet number {} downloaded,time: {}".format(cpt,str(tempo.created_at))) # on la garde pour l'instant
                lastDate=str(tempo.created_at)[:10]
                if(lastDate!=dayDate):
                    newf = os.getcwd()+"/python/corp/data/"+str(query).strip()+"-data_{}.json".format(dayDate)
                    with open(newf,"w",encoding="utf-8") as file2:
                        string=json.dumps({'tweets':[o.dump() for o in Tweets]},indent=4)
                        file2.write(string)
                        Tweets = []
                        dayDate=lastDate
                Tweets.append(tempo)
                cpt+=1
                break
if __name__ == '__main__':
    user = {
        'ck':"D9ZEhBqeHhfkZyvYmAEaEkBu9",
        'cs':"P8IF41bY0snOhokD3LkN67agVxUI3DXDjA2ug436AV5mqOVyyN",
        'act':"295286840-vfHEQEaa50E2ypBXCwkp5gMUL9wgpL6WPSGFykZ2",
        'acs':"Rwy8lkwhnQlubrtyPX5CaF1duOHMAdM8GSRzu6cqba3sc"
    }
    agent = TwitterAgent(user["ck"],user['cs'],user["act"],user["acs"])
    api = agent.get_twitter_client()
    ext = Extractor()
    until = dt.datetime.today()
    since = until - dt.timedelta(days=4)
    print('outside the call')
    #lappath = open(os.getcwd()+"/python/corp/assets/laptops.txt","r") 
    #for q in lappath:
    #    ext.MainCorpExtraction(api,since,dt.datetime.today(),q)
#
    #spath = open(os.getcwd()+"/python/corp/assets/companies.txt","r")
#
    #for query in spath:
    #    ext.MainCorpExtraction(api,since,dt.datetime.today(),query)
#
    smart = open(os.getcwd()+"/python/corp/assets/smartphones.txt","r") 
    for q in smart:
        ext.MainCorpExtraction(api,since,dt.datetime.today(),q)
    print('end of the call')
