# Import our Twitter credentials from credentials.py and tweepy
import tweepy
from credentials import *

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#import other stuff
import sys
import six
import argparse

"""Function decleration"""
def entity_sentiment_text(text):
    """Detects entity sentiment in the provided text."""
    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    document = types.Document(
        content=text.encode('utf-8'),
        type=enums.Document.Type.PLAIN_TEXT)

    # Detect and send native Python encoding to receive correct word offsets.
    encoding = enums.EncodingType.UTF32
    if sys.maxunicode == 65535:
        encoding = enums.EncodingType.UTF16

    result = client.analyze_entity_sentiment(document, encoding)

    for entity in result.entities:
        #salience measures 'importance' if it Google says something isn't important then ignore it
        if entity.salience >= 0.3:
            if entity.name in entitiesDict:
                entitiesDict[entity.name][0] += 1
                entitiesDict[entity.name][1] = (entitiesDict[entity.name][1] + entity.sentiment.score) / entitiesDict[entity.name][0]
            else:
                entitiesDict[entity.name] = [1, entity.sentiment.score]

#  dictionary; key = entityName : value = [numOfOccurences, runningSentimentTotal]
entitiesDict = {}

#parse those inputs
parser = argparse.ArgumentParser()
parser.add_argument('-q', '--query', help ="search for tweets matching a query", action = 'store_true')
parser.add_argument('-t', '--timeline', help ="pull tweets from @comp469 timeline", action ='store_true')
parser.add_argument('-o', '--othertimeline', help ="pull tweets from specified timeline", action ='store_true')
args = parser.parse_args()

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# user timeline/search/default timeline(@comp469)
if args.othertimeline:
    # gets 20 latest tweets from account's timeline
    screenName = input("enter screename or user id of twitter user: ")
    tweets = api.user_timeline(screenName)
elif args.query:
    # get tweets from a search
    searchQuery = input("Enter search query: ")
    tweets = api.search(searchQuery, 'en', True)
else:
    # default to @comp469 timeline
    tweets = api.home_timeline(None,None,50)


#analyze each tweet from collection of tweets
for tweet in tweets:
    entity_sentiment_text(tweet.text)

#find the top mentioned mentioned entities and retweet them w/ sentiment
high = 0
highKey = ""

print(entitiesDict)

for key, value in entitiesDict.items():
    if value[0] > high:
        high = value[0]
        highKey = key

sentiment = ""
if entitiesDict[highKey][1] > 0:
    sentiment = "positive"
elif entitiesDict[highKey][1] < 0:
    sentiment = "negative"
else:
    sentiment = "neutral"

if args.othertimeline:
    print("Most popular entity tweeted about by " + screenName + " is " + highKey + ". The overall sentiment is " + sentiment + ".")
    api.update_status("Most popular entity tweeted about by " + screenName + " is " + highKey + ". The overall sentiment is " + sentiment + ".")
else:
    print("Most popular entity tweeted about " + highKey + ". The overall sentiment is " + sentiment + ".")
    api.update_status("Most popular entity tweeted about " + highKey + ". The overall sentiment is " + sentiment + ".")



