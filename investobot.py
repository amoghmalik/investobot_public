#!/usr/bin/env python
import tweepy
import time
import json
from keys import keys
import ast
import finance_scrape
import analyzer


CONSUMER_KEY = keys['consumer_key']
CONSUMER_SECRET_KEY = keys['consumer_secret']
ACCESS_TOKEN = keys['access_token']
ACCESS_TOKEN_SECRET = keys['access_token_secret']

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)


mentions = api.mentions_timeline(count=1)

comp_ticker = {"google": "GOOG", "apple": "AAPL"}

while True:
	for mention in mentions:
		tw = mention.text
		_, cmd, comp = tw.split(' ')

		print tw
		print cmd, comp
		print mention.user.screen_name

		comp = comp.lower()
		ticker = comp_ticker.get(comp, None)

		price, coef = analyzer.analyzeSymbol(ticker)
		market_fear = finance_scrape.get_fear_score(ticker)

		print (price, coef, market_fear)

		api.update_status(
			"Hello @{}! I think that the {} stock will be at {:.2f} tomorrow - With a Confidence of {:.2f}% and a Bear ratio of {}".format(
				mention.user.screen_name, comp.title(), price, 100 * coef, market_fear))
		
		exit(0)



def getCompanymmand(phrase):
    temp = phrase.split(' ')
    command = temp[0].lower()
    return command

def getCompany(phrase):
    temp = str.split(phrase)
    company = temp[1].lower()
    return company
  
def getTicker(company):
    company = getCompany(phrase)
    tickerTest = stockName[company]
    return tickerTest
    
def getMood(prediction, confidence, marketByNews):
     return "My prediction is " + prediction + ". I am " + str(confidence) + "% confident about it. Market by News: " + marketByNews
     if confidence > 50 and marketByNews == "positive":
        return "You should buy this stock"
     elif confidence > 50 and marketByNews == "negative":
        return "I think that you should not but this stock" 
        
       
    
def getRecomendation(confidence, marketByNews):
     if confidence > 50 and marketByNews == "positive":
        return ". I think that you should buy this stock."
     elif confidence > 50 and marketByNews == "negative":
        return ". I think that you should not but this stock." 
        
def getTweet(tweet):
    return tweet
       
# MAIN
command = getCommand(phrase)
ticker = str(getTicker(phrase))
company = getCompany(phrase)

# TEST - all these print statements
print("The Command is " + command)
print("The Company is " + company)
print("The Ticker is " + ticker)

# TEST - hard coded information
tweet = getMood("101.1", 96, "positive") + getRecomendation(96, "positive")

print(getTweet(tweet))



