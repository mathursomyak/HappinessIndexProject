__author__ = 'skmathur'

from bs4 import BeautifulSoup
from textblob import TextBlob
import numpy as np
import urllib2
import re
import csv
import sys
import unicodedata
import json
import twitter

def makeStateCSV(state, level='all'):

    StateURL = "http://www.usnpl.com/"+state+"news.php"
    CSVname = "C:\Users\skmathur\Documents\GitHub\HappinessIndexProject\StateCSVs\TwitterSentiment_"+state.upper()+".csv"

    # Open the URL to get the review data
    request = urllib2.Request(StateURL)

    try:
        page = urllib2.urlopen(request)
    except urllib2.URLError, e:
        if hasattr(e, 'reason'):
            print 'Failed to reach url'
            print 'Reason: ', e.reason
            sys.exit()
        elif hasattr(e, 'code'):
            if e.code == 404:
                print 'Error: ', e.code
                sys.exit()

    content = page.read()
    soup = BeautifulSoup(content)

    # GETS LINKS FOR TWITTER FEEDS BY STATE
    TwitterFeed = []
    for link in soup.find_all('a'):
        if re.match(r'^T$', link.text) != None:
            TwitterFeed.append(link.get('href'))

    # GET TWITTER USERNAMES FROM LINKS
    usernames = []
    for user in TwitterFeed:
        usernames.append(user[23:len(user)])

    # GRAB RECENT TWEETS FROM EACH NEWSPAPER
    if level=='all':
        tweet_list = []
        state_tweets =[] #for return
        for user in usernames:
            tweets = twitter.get_tweets(user,count=3)
            tweet_list.append({'user':user,'tweets':tweets})
            state_tweets.extend(tweets)
    elif level=='country':
        state_tweets =[] #for return
        for user in usernames:
            tweets = twitter.get_tweets(user,count=4)
            state_tweets.extend(tweets)

    #SENTIMENT ANALYSIS
    def senti(list_of_tweets):
        sentiment,subjectivity = [],[]
        print 'list of tweets',len(list_of_tweets)
        for tweet in list_of_tweets:
            blob = TextBlob(tweet)
            sentiment.append(blob.sentiment.polarity)
            subjectivity.append(blob.sentiment.subjectivity)
        sentiment,subjectivity = np.mean(sentiment),np.mean(subjectivity)#subjectivity[~np.isnan(subjectivity)].mean()
        return {'sentiment':sentiment, 'subjectivity':subjectivity}

    if level=='all':
        for i in range(len(tweet_list)):
            tweets_to_analyze = tweet_list[i]['tweets']
            senti_analy = senti(tweets_to_analyze)
            tweet_list[i].update(senti_analy)

        #SAVE WORK TO A CSV
        headers = ['user', 'sentiment', 'subjectivity','tweets']
        rows = tweet_list

        CSVname = str(CSVname)
        with open(CSVname,'w') as f:
            f_csv = csv.DictWriter(f, headers)
            f_csv.writeheader()
            f_csv.writerows(rows)

    # RETURN A SINGLE VALUE BY STATE
    d = senti(state_tweets)
    sentiment,subjectivity,num_tweets = d['sentiment'],d['subjectivity'],len(state_tweets)
    return sentiment,subjectivity,num_tweets