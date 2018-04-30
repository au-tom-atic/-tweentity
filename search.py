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

entitiesDict = {}

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
        if entity.name in entitiesDict:
            entitiesDict[entity.name][0] += 1
            entitiesDict[entity.name][1] = (entitiesDict[entity.name][1] + float(entity.sentiment.score))
        else:
            entitiesDict[entity.name] = [1, float(entity.sentiment.score)]

# Access and authorize our Twitter credentials from credentials.py
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

queryStr = input('Enter your search query: ')

# gets tweets from timeline
searchResults = api.search(queryStr, 'en', True)

for tweet in searchResults:
    entity_sentiment_text(tweet.text)

print(entitiesDict)
