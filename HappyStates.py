__author__ = 'skmathur'
import TwitterPapers
import csv


states = ['ak','al','ar','az','ca','co','ct','dc','de','fl','ga','hi','ia','id','il','in','ks','ky','la','ma','md','me','mi','mn',
          'mo','ms','mt','nc','nd','ne','nh','nj','nm','nv','ny','oh','ok','or','pa','ri','sc','sd','tn','tx','ut','va','vt','wa','wi','wv','wy']
state_level_senti = []

for state in states:
    print state
    sentiment, subjectivity, countTweets = TwitterPapers.makeStateCSV(state=state, level='country')
    tup = (state, sentiment, subjectivity, countTweets)
    state_level_senti.append(tup)

headers = ['State','Sentiment','Subjectivity','Count Tweets']
filename = "C:\Users\skmathur\Documents\GitHub\HappinessIndexProject\StateCSVs\TwitterSentiment_AllState.csv"
rows = state_level_senti

with open(filename, 'w') as f:
    f_csv = csv.writer(f)
    f_csv.writerow(headers)
    f_csv.writerows(rows)

