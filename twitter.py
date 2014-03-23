from __future__ import unicode_literals
import requests
import json
from requests_oauthlib import OAuth1
from urlparse import parse_qs
import urllib2


REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token"
AUTHORIZE_URL = "https://api.twitter.com/oauth/authorize?oauth_token="
ACCESS_TOKEN_URL = "https://api.twitter.com/oauth/access_token"


CONSUMER_KEY = "9eBhBCzma0TEHSaHrYH0Q"
CONSUMER_SECRET = "wVA8jWGvZFfXNYDGzlcQ4gmfhCSP4yXkA4BlqAyuE"

OAUTH_TOKEN = "89649313-FpspU9zaQGbEXxtp4zSgycVTyp4rIJa59NFlNxDEb"
OAUTH_TOKEN_SECRET = "ZZuRD0iVDVxAk6qZavA3o6DIIlELUpxat3VRPlHoVLUP4"


def setup_oauth():
    """Authorize your app via identifier."""
    # Request token
    oauth = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET)
    r = requests.post(url=REQUEST_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)

    resource_owner_key = credentials.get('oauth_token')[0]
    resource_owner_secret = credentials.get('oauth_token_secret')[0]

    # Authorize
    authorize_url = AUTHORIZE_URL + resource_owner_key
    print 'Please go here and authorize: ' + authorize_url

    verifier = raw_input('Please input the verifier: ')
    oauth = OAuth1(CONSUMER_KEY,
                   client_secret=CONSUMER_SECRET,
                   resource_owner_key=resource_owner_key,
                   resource_owner_secret=resource_owner_secret,
                   verifier=verifier)

    # Finally, Obtain the Access Token
    r = requests.post(url=ACCESS_TOKEN_URL, auth=oauth)
    credentials = parse_qs(r.content)
    token = credentials.get('oauth_token')[0]
    secret = credentials.get('oauth_token_secret')[0]

    return token, secret


def get_oauth():
    oauth = OAuth1(CONSUMER_KEY,
                client_secret=CONSUMER_SECRET,
                resource_owner_key=OAUTH_TOKEN,
                resource_owner_secret=OAUTH_TOKEN_SECRET)
    return oauth

def get_tweets(username, count):
    if not OAUTH_TOKEN:
        token, secret = setup_oauth()
        print "OAUTH_TOKEN: " + token
        print "OAUTH_TOKEN_SECRET: " + secret
        print
    else:
        oauth = get_oauth()
        userstring = '%s'%username
        count = str(count)
        quoteString = urllib2.quote(userstring)
        url = "https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name="+quoteString+"&count="+count+"&exclude_replies=true"
        response = requests.get(url=url, auth=oauth)
        tweets = json.loads(response.content, strict=False)#['statuses']
        #for tweet in tweets:
        #     print tweet['text']
        return tweets
#get_tweets('somyamathur',2)