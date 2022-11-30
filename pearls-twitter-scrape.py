import snscrape.modules.twitter as sntwitter
import pandas as pd
from textblob import TextBlob
import numpy as np
import re
import matplotlib.pyplot as plt
import nltk


query = "(from:aylaazari) until:2022-11-28 since:2021-06-30"
tweets = []
limit = 3790


for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    
    # print(vars(tweet))
    # break
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.username, tweet.content, tweet.likeCount, tweet.retweetCount])
        
df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'num_of_likes', 'num_of_retweet'])
# print(df)

# to save to csv
df.to_csv('tweets.csv')
# df.head()

def cleantweets(tweet):
    stopwords = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from"]
    # if type(tweet) == np.float:
    #     return ""
    temp = tweet.lower()
    temp = re.sub("'", "", temp) # to avoid removing contractions in english
    temp = re.sub("@[A-Za-z0-9_]+","", temp)
    temp = re.sub("#[A-Za-z0-9_]+","", temp)
    temp = re.sub(r'http\S+', '', temp)
    temp = re.sub('[()!?]', ' ', temp)
    temp = re.sub('\[.*?\]',' ', temp)
    temp = re.sub("[^a-z0-9]"," ", temp)
    temp = temp.split()
    temp = [w for w in temp if not w in stopwords]
    temp = " ".join(word for word in temp)
    return temp

df['CleanTweet'] = df['Tweet'].apply(cleantweets)
df['Date'] = pd.to_datetime(df['Date']) 
df['Time'] = df['Date'].dt.time

df['Months'] = pd.DatetimeIndex(df['Date']).month_name()

def TextSubjectivity(tweet):
    return TextBlob(tweet).sentiment.subjectivity

def TextPolarity(tweet):
    return TextBlob(tweet).sentiment.polarity


#%%
df['Subjectivity'] = df['Tweet'].apply(TextSubjectivity)
df['Polarity'] = df['Tweet'].apply(TextPolarity)


df = df.drop(df[df['CleanTweet'] == ''].index)

#%%
def getTextAnalysis(a):
    if a < 0:
        return "Negative"

    elif a == 0:
        return "Neutral"
    else:
        return "Positive"

df["Score"] = df['Polarity'].apply(getTextAnalysis)
df.to_csv('processed_tweets.csv')
# print(df['CleanTweet'])

#%%
positive = df[df['Score'] == "Positive"]
print(str(positive.shape[0]/(df.shape[0])*100) + "% positive tweets")
pos = positive.shape[0]/df.shape[0] * 100

negative = df[df['Score'] == "Negative"]
print(str(negative.shape[0]/(df.shape[0])*100) + "% negative tweets")
neg = negative.shape[0]/df.shape[0] * 100

neutral = df[df['Score'] == "Neutral"]
print(str(neutral.shape[0]/(df.shape[0])*100) + "% neutral tweets")
neutrall = neutral.shape[0]/df.shape[0] * 100


#%%
explode = (0, 0.1, 0)
labels = 'Positive', 'Negative', 'Neutral'
sizes = [pos, neg, neutrall]
colors = ['yellow', 'pink', 'red']

plt.pie(sizes,explode = explode,colors = colors,autopct = '%1.1f%%', startangle = 120)
plt.legend(labels,loc = (-0.05,0.05), shadow = True)
plt.axis('equal')
plt.savefig("Pearls_Sentiment_Analysis.png")




