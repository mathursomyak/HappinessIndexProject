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

states = ['ak','al','ar','az','ca','co','ct','dc','de','fl','ga','hi','ia','id','il','in','ks','ky','la','ma','md','me','mi','mn',
          'mo','ms','mt','nc','nd','ne','nh','nj','nm','nv','ny','oh','ok','or','pa','ri','sc','sd','tn','tx','ut','va','vt','wa','wi','wv','wy']

# Open the URL to get the review data
request = urllib2.Request('http://www.usnpl.com/canews.php') #%states[4]

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
#print len(usernames)

# GRAB RECENT TWEETS FROM EACH NEWSPAPER - there is a limit of 300 requests per day
usernames = usernames[0:50]
tweet_list = []
for user in usernames:
    tweets = twitter.get_tweets(user,count=3)
    tweet_list.append({'user':user,'tweets':tweets})

#tweet_list = [{'tweets': [u'A final heroic act \u2014 Simi Valley teen drowns in river while trying to save his parents: http://t.co/VNgAgWzn2U', u'RT @VCFD_PIO: Hwy 126 TC- IC reporting 3 vehicle TC, 10 patients, 6 transported, 4 refused transport. Beginning to release resources.', u'Walmart store to open April 2 in Newbury Park: http://t.co/pBzpflY2zv'], 'user': 'theacornonline'}, {'tweets': [u'\u0412\u0438\u043d\u043a\u0441 \u0438 \u0441\u043f\u0435\u0446\u0438\u0430\u043b\u0438\u0441\u0442\u044b \u0432\u0438\u0434\u0435\u043e http://t.co/o82rtXD8ph \u0418\u0433\u0440\u043e\u0432\u044b\u0435 \u0430\u0432\u0442\u043e\u043c\u0430\u0442\u044b d\u0430 \u0444\u0430\u043d\u0442\u0438\u043a\u0438 \u0441\u043b\u043e\u0442\u044b crazy fruits http://t.co/c4u4lqikwf @laalaawaee', u'\u043a\u0430\u0442\u0430\u043b\u043e\u0433 \u0441\u0435\u0440\u0432\u0435\u0440\u043e\u0432 minecraft 1 2 5 http://t.co/Lak8pX0yNT \u0447\u0442\u043e \u0434\u0435\u043b\u0430\u0442\u044c \u0445\u0435\u043b\u0443\u0438\u043d\u0441\u043a\u043e\u0439 \u0442\u044b\u043a\u0432\u043e\u0439 \u0432 \u043c\u0430\u0439\u043d\u043a\u0440\u0430\u0444\u0442 http://t.co/qmx7l9GlmZ', u'\u0441\u043e\u0437\u0434\u0430\u0442\u044c \u0431\u0435\u0441\u043f\u043b\u0430\u0442\u043d\u043e \u0441\u0430\u0439\u0442 \u0434\u043b\u044f minecraft http://t.co/DazVPmNutH \u0438\u0433\u0440\u044b \u043d\u0430 \u0434\u0432\u043e\u0438\u0445 \u043c\u0438\u043d\u0438\u043a\u0440\u0430\u0444\u0442 \u0438\u0433\u0440\u0430\u0442\u044c http://t.co/MU6FqC5eMF'], 'user': 'ConejoCalendar'}, {'tweets': [u'MT @SFBaynewsrogers: @CA_Richmond manager Bill Lindsay and @RPDChiefMagnus tour 23rd street today http://t.co/1aIICrYc9E #RichmondCA'], 'user': 'CCTimes'}, {'tweets': [u"Chicanas, Cholas and Chisme last showing tonight at @CASA0101. Don't miss out! http://t.co/jbQZkkwuaV", u'RT @LibrosSchmibros: More on ACA MT @boyleheightsbt: TODAY learn about healthcare enrollment. Food+childcare at St. Teresita 9am-2pm. http:\u2026', u'Chicanas, Cholas, and Chisme celebrates the Latina experience. Final showing tonight @CASA0101 http://t.co/PVeidtOWRS'], 'user': 'boyleheightsbt'}, {'tweets': [u'"He had American Canyon in his heart" \u2014 http://t.co/Cn67EpbyWj', u'Goodwill opens store in American Canyon http://t.co/PIvMSXI3Nq', u'Double amputee Marine stops in American Canyon on cross-country ride http://t.co/8xFNjq8rbf'], 'user': 'AmCanEagle'}, {'tweets': [u'Movie review: \u2018Cesar Chavez\u2019 a story that needed to be told http://t.co/Ingn4hXMYJ #Show', u"Vietnam veterans get long-awaited 'welcome home' with Texas memorial http://t.co/zIFWysGHbe #News", u'Undocumented immigrant driving with 15 AK-47s in trunk gets 40 months in prison http://t.co/NcrgHTBsoc #Latinos'], 'user': 'LatinoTimes'}, {'tweets': [u'Art gallery to open next week - The Delta Gallery of the Arts at The Streets of Brentwood will debut during a thre... http://t.co/WpBlnIetSZ', u'BI Lions host pancake breakfast - The Bethel Island Lions Club hosts pancake breakfast \u2013 complete with sausa... http://t.co/H1O2UViHbK', u'Casa Ferratt caters to customers - Oakley\u2019s newest restaurant Casa Ferratt, located on the corner of Main and ... http://t.co/pR9dMfDd82'], 'user': 'thepress_net'}, {'tweets': [u'RT @RyanBurnsy: Congrats to my friends and former @ncj_of_humboldt colleagues for their latest awards. They do good journalism. http://t.co\u2026', u'First Liquor Trucks Leave the Pulp Mill http://t.co/7ixJXIfenM', u"You've settled in at your desk, finished your coffee \u2014 time to think about lunch. Crab sandwich? http://t.co/NS7ghBHn5h"], 'user': 'ncj_of_humboldt'}, {'tweets': [u'Mug shots are posted for the inter-state train-hopper/murder arrests report GCM broke early yesterday morning http://t.co/FODS6vljTh', u'Police make inter-state arrests in Roseville train-hopper murder http://t.co/sWSk5t7yAF', u'After tens months of investigation, GCM and The Press Tribune are the first in California to break this story: http://t.co/Ox5pGl4yp8'], 'user': 'AuburnJournal'}, {'tweets': [u"PHOTO CONTEST: Let's see your best telephoto shots! Details here: http://t.co/hlmAz3thO1", u'Stay off the 99 -- a big-rig burning on an overpass is causing chaos in the area: https://t.co/B6Uf0KlVYl', u'RT @TheBakosphere: Former NFL player selling Bakersfield mansion for $2.8 million, complete with "Star Trek" theater: http://t.co/YYQjtNAQy\u2026'], 'user': 'bakersfieldcali'}]

#SENTIMENT ANALYSIS
def senti(list_of_tweets):
    sentiment,subjectivity = [],[]
    for tweet in list_of_tweets:
        blob = TextBlob(tweet)
        sentiment.append(blob.sentiment.polarity)
        subjectivity.append(blob.sentiment.subjectivity)
    sentiment,subjectivity = np.mean(sentiment),np.mean(subjectivity)
    return {'sentiment':sentiment, 'subjectivity':subjectivity}

for i in range(len(tweet_list)):
    tweets_to_analyze = tweet_list[i]['tweets']
    senti_analy = senti(tweets_to_analyze)
    tweet_list[i].update(senti_analy)
print tweet_list

#SAVE WORK TO A CSV
headers = ['user', 'sentiment', 'subjectivity','tweets']
rows = tweet_list

with open('TwitterPapers.csv','w') as f:
    f_csv = csv.DictWriter(f, headers)
    f_csv.writeheader()
    f_csv.writerows(rows)