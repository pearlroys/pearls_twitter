# Sentiment_Analysis_of_Pearl's_Tweets_Using_PowerBI

Sam Harris a modern intellectual and someone I highly respect left twitter in November this year, and described his leaving as a way to look better at society. Apparently he had resulted to blocking people en-masse and realized his perception of the world and how he viewed people had changed due to his interaction on twitter. 
I then became interested in my impact to the society on twitter.
I decided to scrape all my tweets since I joined twitter in June 2021 and palpate the temperance of my tweets using sentiment analysis.

# The Documentation includes:
- Data Gathering and Transformation
- Sentiment Analysis
- Visualization using a Power Bi dashboard
- Conclusion
<img width="802" alt="Screenshot 2022-12-07 at 15 16 39" src="https://user-images.githubusercontent.com/103274172/206217614-233edec9-ab57-43a2-b506-4377832562fb.png">



# Data Gathering and Transformation
The process of mining the tweets was easy and straightforward. Snscrape is a simple and powerful library that helped make the process easy. I had tried to use the twitter API (tweepy) but was not given access even after several attempts to apply. I scraped these from my page 'Date', 'User', 'Tweet', 'num_of_likes', 'num_of_retweet'.
The result of the query can be seen in a dataframe and was later stored in a csv file.
```python 
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
```

# Transformation

Data preprocessing: The bulk of the project lies here. For the sentiment analysis to be carried out this stage needs to be done accurately. Data pre-processing depends on the nature of data you are working on and what needs to be changed however, there are some transformations that are fixed for the sentiment analysis to be carried out. These pre-processing in no particular order include:

- Converting the words to lower case: During the preprocessing stage, the tweet column is converted to lower case words to make the words uniform.
- Removing Url links, digits, punctuation, emojis and every other thing that may not be necessary for the sentiment analysis
- Tokenizing the tweets column that is breaking the sentence down into bits of words
- Removing stop words: This are word that don’t give meaning to the context of a sentence example is, the etc.
- Lemmatizing words: This is to get the base of words ie bags the lemmatized form is bag.

A new column called CleanTweet is created and can be seen below.
`df['CleanTweet'] = df['Tweet'].apply(cleantweets)`

# Sentiment Analysis
After data wrangling/pre-processing, TextBlob library is used to get the level of the text polarity; that is, the value of how good, bad or neutral the text is which is between the range of 1 to -1. A condition is set to get the sentiment which is set at < 0 is positive, == 0 is neutral and > 1 is negative.

# Data Visualization & Power BI Report
To visualize the data and tell a more compelling story, I will be using Microsoft Power BI.
Python is not the best tool for visualization because its visual is not appealing to the eyes. 


<img width="879" alt="Pearl's Tweets" src="https://user-images.githubusercontent.com/103274172/206230956-ca096f84-4b7b-489a-adb8-2996d75ab59a.png">

My most liked tweet got over a thousand likes because from my personal opinion it was a positive tweet but somehow textblob construed it as negative.
TextBlob is a python library for Natural Language Processing (NLP).TextBlob actively used Natural Language ToolKit (NLTK) to achieve its tasks. NLTK is a library which gives an easy access to a lot of lexical resources and allows users to work with categorization, classification and many other tasks. TextBlob is a simple library which supports complex analysis and operations on textual data. It is obviously not error free but still gives us a fairly decent idea on the sentiments attached to our conversations.
# Conclusion
Overall, I'd say my tweets have been decent, but I could definitely do better at communicating my thoughts in a positive light. After all, what are we doing if we don't leave the lives we encounter (virtually or physically) in a better place than when we first did?





