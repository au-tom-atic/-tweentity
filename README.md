# COMP 469 Project

This project is an attempt to analyze sentiment(positive or negative opinion/viewpoint/attitude) of different entities(who/what/where) in tweets. [Our example twitter](https://twitter.com/comp469) follows various NBA related accounts, and focusing on analyzing NBA content on twitter.

## Getting Started 

### Prerequisites
* [Python3](https://www.python.org/download/releases/3.0/) 
* [pip](https://pypi.org/project/pip/)

In order to run the script(Professor, skip to step 4):
1. Register your Twitter App, and find your tokens/keys
2. Create a `credentials.py` that stores the values of your Twitter tokens/keys
3. Register your app on Google Cloud, turn on Natural Language API, download JSON file containing your API key
4. Set envirnoment variable `GOOGLE_APPLICATION_CREDENTIALS` to the path of JSON file containing your Google API key
5. `pip3 install -r requirements.txt` should install all libraries
6. `python3 analyze.py -h` for all options
  

## Built With:
* [Python3](https://www.python.org/download/releases/3.0/) - you know what Python is
* [tweepy](http://tweepy.readthedocs.io/en/v3.6.0/index.html) - Python library that provides a wrapper for Twitter API
* [Google Cloud Natural Language](https://cloud.google.com/natural-language/) - Google Cloud API for Natural Language analysis
