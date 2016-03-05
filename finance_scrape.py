import urllib
from bs4 import BeautifulSoup as bs 
import requests
import unicodedata
import json

def get_news(companyName):
    urlFirst = "https://www.google.co.uk/finance/company_news?q=NASDAQ%3A"
    urlLast = "&ei=xbLaVqGTBJeVUqeWmqgI"
    url = urlFirst+companyName+urlLast
    source_code = urllib.urlopen(url)
    plain_text = source_code.read()
    soup = bs(plain_text, "html.parser")
    headLines = soup.findAll('div', {'class':'g-section news sfe-break-bottom-16'})
    passingString = ""
    for lines in headLines:
        array = lines.getText().split('\n')
        array = map(lambda t: unicodedata.normalize('NFKD', t).encode('ascii','ignore'), array)
        tempString =" " + array[2] + array[10]
        passingString += tempString


    return urllib.quote_plus(passingString)   


import requests as r
from requests.auth import HTTPBasicAuth

UN = "aee0f544-c56c-49f3-a529-43ef19047960"
PW = "elnmzTVIm1cI"

def get_degree_sentiment(companyName):
    news = get_news(companyName)
    return r.get("https://gateway.watsonplatform.net/tone-analyzer-beta/api/v3/tone?version=2016-02-11&text={}".format(news),
                                                                                                                  auth=HTTPBasicAuth(UN, PW)).text

def get_fear_score(companyName):
    sentiment = get_degree_sentiment(companyName)
    data = json.loads(sentiment)
    return data['document_tone']['tone_categories'][0]['tones'][2]['score']  # fear