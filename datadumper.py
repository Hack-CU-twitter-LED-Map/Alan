import dataset
import os
from datafreeze import freeze
import time
import re 
import csv


def csvReader():
    with open('tweets.csv', 'r') as file:
        has_header = csv.Sniffer().has_header(file.read(1024))
        file.seek(0)
        reader = csv.reader(file)
        if has_header:
            next(reader)
        for row in reader:
            cleaned_tweet = process(row[1])
            tweetloc = row[2]
            scorer(cleaned_tweet, location)

def process(raw_tweet):
    raw_tweet= re.sub(r'[^\w\s]','',raw_tweet)
    raw_tweet=raw_tweet.lower()
    return raw_tweet

def scorer(tweet, location):
    positive=0
    negative=0
    tweet=tweet.split()
    for i in tweet:
        if i in ignorew:
            continue
        elif i in posw:
            positive+=1
        elif i in negw:
            negative-=1
    if positive>negative:
        return 1
    if negative>positive:
        return -1
    else:
        return 0



posw =[None]* 2012
negw= [None]* 2020
ignorew =[None]*51
count = 0

f=open("poswords.txt", "r")
for l in f:
    l=l.strip()
    posw[count]=l
    count+=1
f.close()
count=0

f= open("negwords.txt")
for l in f:
    l=l.strip()
    negw[count]=l
    count+=1
f.close()
count=0

f=open("ignoreWords.txt")
for l in f:
    l=l.strip()
    ignorew[count]=l
    count+=1
f.close()

def main(): 

    

	while True:
		try:
			os.remove("tweets.csv")
		except:
			pass

		database = dataset.connect("sqlite:///tweets.db")

		result = database["tweets"].all()

		freeze(result, format='csv', filename="tweets.csv")

		csvReader()

		table = database["tweets"]
		table.delete()

		time.sleep(300.0)

    


if __name__ == "__main__":
    main()

