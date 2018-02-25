#this is the data processing file
#this file is a small workspace for the data processing fuctions fuctions
#the fuctions will be inplemented in the datagetter.py file
import re
import time
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
            print(cleaned_tweet, scorer(cleaned_tweet))

def process(raw_tweet):
    raw_tweet= re.sub(r'[^\w\s]','',raw_tweet)
    raw_tweet=raw_tweet.lower()
    return raw_tweet

def scorer(tweet):
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

    csvReader()

    


if __name__ == "__main__":
    main()
