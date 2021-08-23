
from datetime import datetime
from data.companies import Company
from data.laptops import Laptop
from data.laptops import LDiscription
from data.smartphones import Smartphone
from data.smartphones import SDiscription
from data.extracted_data import EData
from data.tweet import Tweet, Score

def create_smartphone(name,manifactor,release,discription):
    phone = Smartphone()
    phone.name = name
    phone.manifactor = manifactor
    phone.date_of_release = release
    phone.discription = discription
    phone.save()
    return phone

def find_phone_by_name(name) :
    phone = Smartphone.objects(name=name).first()
    return phone

def add_phone_data(name,bdate,edate,total,pos,neg,neut,tweets):
    
    doc = EData()
    
    for t in tweets:
        tweet = Tweet()
        tweet.t_id = t['id']
        tweet.t_text = t['text']
        tweet.post_time = datetime.strptime(t['created_at'],'%Y-%m-%d %H:%M:%S')
        tweet.lang = t['lang']
        tweet.retweet_count = t['retweet_count']
        tweet.fav_count = t['favorite_count']
        tweet.mentions = [m for m in t['mention'] ]
        tweet.label = t['label']
        score = Score()
        note = t['note']
        score.positivity = note['positivity']
        score.negativity  = note['negativity']
        score.classification = note['classification']
        tweet.score = score
        tweet.user_id = t['user_id']
        tweet.save()
        doc.tweets_ids.append(tweet.id)
        
    doc.query = name
    doc.begin_date = bdate
    doc.end_date = edate
    doc.total_tweets = total
    doc.negative_tweets = neg
    doc.positive_tweets = pos
    doc.neutral_tweets = neut
    doc.save()
    phone = Smartphone.objects(name=name).first()
    phone.extracted_data_ids.append(doc.id)
    phone.save()
