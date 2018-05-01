# Import our Twitter credentials from credentials.py
import tweepy
from credentials import *

# Imports the Google Cloud client library
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

#needed
import sys
import six
import argparse

#  dictionary; key = entityName : value = [numOfOccurences, runningSentimentTotal]
entitiesDict = {}

#parse those inputs
parser = argparse.ArgumentParser()
parser.add_argument('-s', '--search', help ="search for term(takes one argument)", type=str)
parser.add_argument('-t', '--timeline', help ="pull from timeline", action ='store_true')
args = parser.parse_args()

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
        if entity.salience >= 0.5:
            if entity.name in entitiesDict:
                entitiesDict[entity.name][0] += 1
                entitiesDict[entity.name][1] = (entitiesDict[entity.name][1] + entity.sentiment.score)
            else:
                entitiesDict[entity.name] = [1, entity.sentiment.score]

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# did we wanna search or use the timeline?
if args.timeline:
    # gets at most 150 tweets from account's timeline
    tweets = api.home_timeline(None,None,150)
else:
    tweets = api.search(args.search, 'en', True)

#analyze each tweet from timeline
for tweet in tweets:
    entity_sentiment_text(tweet.text)

#find the top mentioned 3 mentioned entities and retweet them w/ sentiment
#just printing the dictionary rn
print(entitiesDict)



