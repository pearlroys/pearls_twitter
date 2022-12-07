import snscrape.modules.twitter as sntwitter
import pandas as pd
from textblob import TextBlob
import numpy as np
import re
import matplotlib.pyplot as plt
import nltk

# user to scrape from, number of tweets to scrape
query = "(from:aylaazari) until:2022-11-28 since:2021-06-30"
tweets = []
limit = 3790


for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    
   
    # tweet values to scrape
    if len(tweets) == limit:
        break
    else:
        tweets.append([tweet.date, tweet.username, tweet.content, tweet.likeCount, tweet.retweetCount])
# save to a dataframe  
df = pd.DataFrame(tweets, columns=['Date', 'User', 'Tweet', 'num_of_likes', 'num_of_retweet'])


# to save to csv
df.to_csv('tweets.csv')


def cleantweets(tweet):
    """ a function to clean the tweets by removing stop words, 
    smileys and other things that would interefere with analysis

    Args:
        tweet (str): tweets scarped

    Returns:
        _type_: tweets having being cleaned
    """
    stopwords = ["for", "on", "an", "a", "of", "and", "in", "the", "to", "from"]
    
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

# to remove rows in which tweets that are empty
df = df.drop(df[df['Tweet'] == ''].index) 

# append cleantweets to the dataframe, and other necessary columns neeeded
df['CleanTweet'] = df['Tweet'].apply(cleantweets)
df['Date'] = pd.to_datetime(df['Date']) 
df['Time'] = df['Date'].dt.time
#appends a column to the df that extracts just the month when the tweets were made
df['Months'] = pd.DatetimeIndex(df['Date']).month_name()


# sentiment analysis
def TextSubjectivity(tweet):
    return TextBlob(tweet).sentiment.subjectivity

def TextPolarity(tweet):
    return TextBlob(tweet).sentiment.polarity


#%%
# adds subjectivity and polarity column to the dataframe
df['Subjectivity'] = df['CleanTweet'].apply(TextSubjectivity)
df['Polarity'] = df['CleanTweet'].apply(TextPolarity)



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
# gives percentage of tweets are positive, negative or neutral
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
#plots pie chart with the result from the sentiment analysis
explode = (0, 0.1, 0)
labels = 'Positive', 'Negative', 'Neutral'
sizes = [pos, neg, neutrall]
colors = ['yellow', 'pink', 'red']


plt.pie(sizes,explode = explode,colors = colors,autopct = '%1.1f%%', startangle = 120)
plt.legend(labels,loc = (-0.05,0.05), shadow = True)
plt.axis('equal')
plt.savefig("Pearls_Sentiment_Analysis.png")




