# Import our Twitter credentials from credentials.py
import tweepy
from credentials import *

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# gets tweets from timeline
searchResults = api.search('news', 'en', True)

for tweet in searchResults:
    print(tweet.text)
