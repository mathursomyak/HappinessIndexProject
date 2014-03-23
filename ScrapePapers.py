__author__ = 'skmathur'
import Happiness as hp
from bs4 import BeautifulSoup
import sys
import urllib2

CA_papers_dict, newspaper_links, county_names = hp.CaliPapers()
"""
print newspaper_links

n_dict ={}
for l in range(len(newspaper_links)):
    request = urllib2.Request(newspaper_links[l])
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
    print soup.prettify()
"""

request = urllib2.Request('http://www.siskiyoudaily.com/')

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
#print 'THE SOUP',soup.prettify()
print 'THE TEXT',soup.text