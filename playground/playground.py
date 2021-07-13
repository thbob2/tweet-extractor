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

nltk.download("stopwords")
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.callbacks import EarlyStopping

df = pd.read_csv(os.getcwd()+"/playground/playdata/train.csv")

#print(df.head())

df = df.drop(['id'],axis=1)
df.dropna(inplace=True)
print(df.head())

#!
#! if label =0 positive
#! if label = 1 negative 


df['polarity_rating'] = df['label'].apply(lambda x: 'Positive' if x == 0 else 'Negative')

print(df.head())

sns.set_style('whitegrid')
sns.countplot(x='label',data=df, palette='YlGnBu_r')
#plt.show()

# data processing
df_pos = df[df['polarity_rating'] == 'Positive'][0:3000]
df_neg = df[df['polarity_rating'] == 'Negative']

#sample negative and and create final dataset

df_Neg_over = df_neg.sample(5000,replace=True)
df = pd.concat([df_pos,df_Neg_over],axis=0)

#text processing
def get_text_processing(text):
    stpword = stopwords.words('english')
    no_punctuation = [char for char in text if char not in string.punctuation]
    no_punctuation = ''.join(no_punctuation)
    return ' '.join([word for word in no_punctuation.split() if word.lower() not in stpword])


df['cl_tweet'] = df['tweet'].apply(get_text_processing)

#print(df.head())
df = df[['cl_tweet', 'polarity_rating']]
one_hot = pd.get_dummies(df['polarity_rating'])
df.drop(['polarity_rating'],axis=1, inplace=True)
df = pd.concat([df,one_hot],axis=1)

print(df.head())

#apply train test split

X = df['cl_tweet'].values
Y = df.drop("cl_tweet", axis=1).values
X_train, X_test, Y_train, Y_test = train_test_split(X,Y,test_size=0.30, random_state=42)
#! apply vectorization
vect = CountVectorizer()
X_train = vect.fit_transform(X_train)
X_test = vect.transform(X_test)

#! apply frequency inverse document frequency 

tfidf = TfidfTransformer()
X_train = tfidf.fit_transform(X_train)
X_test = tfidf.transform(X_test)
X_train = X_train.toarray()
X_test = X_test.toarray()

#*build a deeplearing model 

model = Sequential()
model.add(Dense(units=12673, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(units=4000, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(units=500, activation="relu"))
model.add(Dropout(0.5))
model.add(Dense(units=3, activation="softmax"))
opt = tf.keras.optimizers.Adam(learning_rate=0.001)
model.compile(loss="categorical_crossentropy", optimizer=opt, metrics=["accuracy"])
early_stop = EarlyStopping(monitor="val_loss", mode="min", verbose=1, patience=2)

model.fit(
    x=X_train,
    y=Y_train,
    batch_size=256,
    epochs=100,
    validation_data=(X_test, Y_test),
    verbose=1,
    callbacks=early_stop,
)