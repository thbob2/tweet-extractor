from json.decoder import JSONDecodeError
import regex as re
import pickle
import json
import pandas as pd
import nltk 
import emoji

import textblob
from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer 
from textblob.classifiers import NaiveBayesClassifier
from os import error, listdir
from os.path import isfile, join
import os 
import datetime as dt

words = set(nltk.corpus.words.words())

def feeling(text):
    result = TextBlob(text)          
    if(result.sentiment[0]>0): 
        return "positive".format(result.sentiment[0])
    elif(result.sentiment[0]==0): 
        return"nutral".format(result.sentiment[0])
    else: 
        return "negative".format(result.sentiment[0])


# naive bayes felling analyser 
def feelingBayes(text):
    result = TextBlob(text,analyzer=NaiveBayesAnalyzer())
    return result.sentiment


def cleaner(tweet):
    tweet = re.sub("@[A-Za-z0-9]+","",tweet) #Remove @ sign
    tweet = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet) #Remove http links
    tweet = " ".join(tweet.split())
    tweet = ''.join(c for c in tweet if c not in emoji.UNICODE_EMOJI) #Remove Emojis
    tweet = tweet.replace("#", "").replace("_", " ") #Remove hashtag sign but keep the text
    tweet = " ".join(w for w in nltk.wordpunct_tokenize(tweet) \
         if w.lower() in words or not w.isalpha())
    return tweet



text ="I'm so happy! Sister bought me a new phone for early b-day gift! So happy! #Samsung #S4"

text = cleaner(text)

print(text)
print(feeling(text))

result = feelingBayes(text)
try:
    print("in the try")
    print(result)
except:
    print(" in the except")
    for x in result:
        print(x)