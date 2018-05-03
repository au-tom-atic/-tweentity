"""
COMP 469 - FINAL PROJECT
Checkout @comp469 on twitter

@comp469 follows a number of twitter accounts who regularly feature NBA content
We try to analyze who/what these accounts are tweeting about, and how they feel about the subject on average
You can also search twitter
or analyze the timeline of a twitter user

see README.md for more instructions
run 'python3 analyze.py -h' for all options 
"""

from credentials import *

# Import our Twitter credentials from credentials.py and tweepy
import tweepy

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
        if entity.salience >= 0.25:
            print(u'Name: "{}"'.format(entity.name))
            print(u'Sentiment: {}\n'.format(entity.sentiment.score))
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
parser.add_argument('-t', '--timeline', help ="pull tweets from authenticated user's timeline", action ='store_true')
parser.add_argument('-o', '--othertimeline', help ="pull tweets from specified timeline", action ='store_true')
args = parser.parse_args()

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# user timeline/search/default timeline(@comp469)
if args.othertimeline:
    # gets 20 latest tweets from account's timeline
    userInput = input("enter screename or user id of twitter user: ")
    tweets = api.user_timeline(userInput)
elif args.query:
    # get tweets from a search
    userInput = input("Enter search query: ")
    tweets = api.search(userInput, 'en', True)
else:
    # default to @comp469 timeline
    tweets = api.home_timeline(None,None,50)
    userInput = "@comp469"


#analyze each tweet from collection of tweets
for tweet in tweets:
    entity_sentiment_text(tweet.text)

#find the top mentioned mentioned entities and retweet them w/ sentiment
high = 0
highKeys = []

print(entitiesDict)

for key, value in entitiesDict.items():
    if value[0] > high:
        #new high occurance
        high = value[0]
        highKeys.clear()
        highKeys.append(key)
    elif value[0] == high:
        #matches # of occurences
        high = value[0]
        highKeys.append(key)

print("top entities: \n")
print(highKeys)

for key in highKeys:
    sentiment = ""
    if entitiesDict[key][1] == 0.0:
        sentiment = "neutrally"
    elif entitiesDict[key][1] > 0:
        if entitiesDict[key][1] < 0.25:
            sentiment = "slightly positively"
        elif entitiesDict[key][1] < 0.75:
            sentiment = "positively"
        else:
            sentiment = "very positively"
    elif entitiesDict[key][1] < 0:
        if entitiesDict[key][1] > -0.25:
            sentiment = "slightly negatively"
        elif entitiesDict[key][1] > -0.75:
            sentiment = "negatively"
        else:
            sentiment = "very negatively"
    if args.othertimeline:
        print("Analysis shows that " + userInput + " is tweeting about " + key + " " + sentiment)
        api.update_status("Analysis shows that " + userInput + " is tweeting about " + key + " " + sentiment)
    elif args.query:
        print("Search results for " + userInput + " show that " + key + " is trending " + sentiment)
        #dont want to retweet search results
        #api.update_status("Search results for " + userInput + " show that " + key + " is trending " + sentiment)
    else:
        print("Anaylsis shows that my timeline is tweeting about " + key + " " + sentiment)
        api.update_status("Anaylsis shows that my timeline is tweeting about " + key + " " + sentiment)





