#?#############################################################
#?  imports                                                   #
#?#############################################################
import os
import pandas as pd
import numpy as np
import seaborn as sns
import re
import string
from string import punctuation
import nltk
from nltk.corpus import stopwords
import json
nltk.download("stopwords")
import matplotlib.pyplot as plt
import textblob as tb


def readJson(path):
    with open(path,'r') as f:
        return json.loads(f.read())

def feeling(text):
    result = tb.TextBlob(text)           
    if(result.sentiment[0]>0): 
        return "positive".format(result.sentiment[0])
    elif(result.sentiment[0]==0): 
        return"nutral".format(result.sentiment[0])
    else: 
        return "negative".format(result.sentiment[0])
    
def isFbi(tweet):
    name = "FBI"
    text = str(tweet)
    if (re.search(r'\b{}\b'.format(name.lower()),text) or re.search(r'\b{}\b'.format(name.upper()),text)):
        return text

def get_text_processing(text):
    stpword = stopwords.words('english')
    no_punctuation = [char for char in text if char not in string.punctuation]
    no_punctuation = ''.join(no_punctuation)
    return ' '.join([word for word in no_punctuation.split() if word.lower() not in stpword])


data = readJson(os.getcwd()+"/python/corp/data2.0/smartphones/iPhone SE (2nd generation)/iPhone SE (2nd generation)-data_2021-01-21.json")

df = pd.json_normalize(data,record_path=['tweets'])
#print(df.head())
df = df[['text','favorite_count','retweet_count']]
print(df.head())

df['polarity_rating'] = df['text'].apply(feeling)
df['cl_text'] = df['text'].apply(get_text_processing)
sns.set_style('whitegrid')
sns.countplot(x='polarity_rating',data=df, palette='summer')
plt.show()
df = df[['cl_text', 'polarity_rating','favorite_count','retweet_count']]
one_hot = pd.get_dummies(df['polarity_rating'])
df.drop(['polarity_rating'],axis=1, inplace=True)
df = pd.concat([df,one_hot],axis=1)
#df['text'] = df['text'].apply(isFbi)
print(df.head())
