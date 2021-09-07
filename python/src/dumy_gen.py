import datetime as dt
import json
import os
from filtor import readJson
import random
def dummer():
    dumy_dir1 = os.getcwd()+"/python/corp/data2.0/companies/NZXT/"
    dumy_dates = []
    dirs = os.listdir(dumy_dir1) 
    dummies = []
    for d in dirs:
        total = 0
        pos = 0
        neg = 0 
        date = d.split("_")[1].split(".")[0]
        date = dt.datetime.strptime(date,'%Y-%m-%d')
        date = date + dt.timedelta(days=7)
        tweets = readJson(os.path.join(dumy_dir1,d)) 
        for tweet in tweets['tweets']:
            score = tweet['note']
            if score['classification'] == "pos":
                pos += 1
            else:
                neg +=1
            total +=1 
        dummies.append({
            'date':date.strftime('%Y-%m-%d') ,
            'pos' : pos,
            'neg': neg,
            'total': total,
            'sales' : 0
        })

    for dumm in dummies :
        if(dumm['neg']*100/dumm['total']>=35.0) and dumm['neg'] >= 200:
            dumm['sales'] = random.randint(20000,30000)
        else:
            dumm['sales'] = random.randint(80000,90000)

    with open(os.getcwd()+"/python/corp/dumm-nzxt.json","w") as writor:
        json.dump({'dummies':[o for o in dummies]},writor,indent=4,ensure_ascii=False)

if __name__ == '__main__':
    n  = random.randint(80000,90000)
    print(n)
    dummer()
    