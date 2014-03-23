__author__ = 'skmathur'

from bs4 import BeautifulSoup, Comment
import urllib2
import re
import csv
import sys
import unicodedata

def CaliPapers():
    # Open the URL to get the review data
    request = urllib2.Request('http://www.usnpl.com/canews.php')

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
    #print soup.prettify()

    counties = []
    counties_json = soup.find_all('b')
    for c in counties_json: counties.append(c.text)
    counties = counties[7:502]

    # GETS LINKS FOR ALL CALIFORNIA NEWSPAPERS
    i = -1
    CA_newspapers = []#{}
    for link in soup.find_all('a'):
        i+=1
        if i < 65: continue     #before it gets to the newspapers
        if re.match(r'^([ACFTWV]|[a-z][a-z]|here)$', link.text) == None:
            CA_newspapers.append(link.get('href'))
        if i > 2946: break      #after the newspapers

    papers = {}
    for i in range(len(CA_newspapers)):
        #print CA_newspapers[i], counties[i]
        papers.update({i:{'county':counties[i], 'news':CA_newspapers[i]}})

    return papers, CA_newspapers, counties



