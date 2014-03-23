__author__ = 'skmathur'
__author__ = 'skmathur'

from bs4 import BeautifulSoup, Comment
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

# GRAB RECENT TWEETS FROM EACH NEWSPAPER
text = []
i = 0
for user in usernames:
    if i > 5: break
    print(twitter.get_tweets(user,count=3))
    i +=1
#print text