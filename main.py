import tweepy
import dataset
import os
from datafreeze import freeze
import re
import csv
import json
import time
from html.parser import HTMLParser



database = dataset.connect("sqlite:///tweets.db")
table = database["tweets"]

#creating empty arrays to hold good, bad, and ignore words from text files
posw =[None]* 2012
negw= [None]* 2020
ignorew =[None]*51


count = 0
#adding the good words
f=open("poswords.txt", "r")
for l in f:
    l=l.strip()
    posw[count]=l
    count+=1
f.close()
count=0
#adding the bad words
f= open("negwords.txt")
for l in f:
    l=l.strip()
    negw[count]=l
    count+=1
f.close()
count=0
#adding the ignore words
f=open("ignoreWords.txt")
for l in f:
    l=l.strip()
    ignorew[count]=l
    count+=1
f.close()

time_start = time.time()

#dictionary of cities and their tweet values
city_scores = dict()

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
            score = scorer(cleaned_tweet, tweetloc)

def process(raw_tweet):
    raw_tweet= re.sub(r'[^\w\s]','',raw_tweet)
    raw_tweet=raw_tweet.lower()
    return raw_tweet

def scorer(tweet, location):
    positive=0
    negative=0
    value = 0
    tweet=tweet.split()
    for i in tweet:
        if i in ignorew:
            continue
        elif i in posw:
        	positive += 1
        elif i in negw:
        	negative += 1
    if positive>negative:
        value = 1
    if negative>positive:
        value = -1
    if location in city_scores:
    	city_scores[location].append(value)
    else:
    	city_scores[location] = [value]
    return value



def dumper():
    #dump the database into the csv file
    database = dataset.connect("sqlite:///tweets.db")

    result = database["tweets"].all()

    #tweets.db can not be empty at this point!
    freeze(result, format='csv', filename="tweets.csv")

    table = database["tweets"]
    table.delete()

    #analyze each line in the csv file
    csvReader()

    avg_city_scores = {}


    for key, value in city_scores.items():
        avg_city_scores[key] = (sum(value)/ float(len(value)))
    print("###########################################")
    print(avg_city_scores)

    scores = ""

    for city in cities:
        if city in avg_city_scores:
            if avg_city_scores[city] < -0.5:
                s = 0
            elif (-0.5 < avg_city_scores[city] < 0):
                s = 1
            elif (avg_city_scores[city] == 0):
                s = 2
            elif (0 < avg_city_scores[city] < 0.5):
                s = 3
            else:
                s = 4
            scores += str(s)
            scores += '\n'
        else:
            scores += '2\n'

    with open('scores.txt', 'w') as file:
        file.write(scores)

    
    city_scores.clear()

    os.remove("tweets.csv")

    #erase the database tweets table

    

    try:
        os.delete("tweets.csv")
    except:
        pass
    #wait for five minutes, then redo the above code

#List of cities to check against status.user.location
cities = ["Denver", "Colorado Springs", "Aurora", "Fort Collins", "Lakewood", "Thorton", "Pueblo", "Arvada", "Westminster", "Centennial", "Boulder"]

class StreamListener(tweepy.StreamListener):

    
    def on_status(self, status):
        global time_start
        if ((time.time() - time_start) >600):
            dumper()
            time_start = time.time()
		#overriding the listener class method "on_status" to focus on tweets sent, not dm's or deleting tweets
        if status.retweeted:
            return
        if status.user.location:
            for city in cities:
                if city in status.user.location:
                    try:
                        table.insert(dict(text=status.text, location = city))
                        jsono= status._json
                        print(jsono["user"]["name"])
                        print("@",jsono["user"]["screen_name"])
                        if jsono["truncated"]:
                            print("Said: ",jsono["extended_tweet"]["full_text"])
                            print("")
                        else:
                            print("Said: ",jsono["text"])
                        print("from, ", jsono["user"]["location"])
                        print("")
                        print("")
                    except:
                        print("failed to add")
                        pass

def on_error(self, status_code):
        if (status_code == 420):
            #we're being rate limited!
            print("rate limited")
            return False

#GeoBox location with coordinates in CSV format
#Created with http://boundingbox.klokantech.com/
ColoradoGeoBox = [-109.242,36.8211,-101.7932,41.1649]

#keys for access to Twitter API; they need to be moved to a text file
consumer_key =  "yvpg4uTgfmfBuQcHKSfGzFsd0" #put into text file for security #API Key
consumer_secret = "UZvyD8ZQURRUkCaS7JSAdKKYPzB6ZqHWfFIpvrQrINXvnY0jqp" #API Secret 
access_token = "589306615-SAoJfgRt33KHVxmxUWxYerpKGtUHsY1HEag3cChU" 
access_token_secret = "3Nn2YlTvm2y7uGjIBUrxJwJhNpxW2BzWw1zmVG5acY38q"

#tweepy setup for authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#creating an api object to pull data from Twitter
api = tweepy.API(auth)

stream_listener = StreamListener()

stream = tweepy.Stream(auth=api.auth, listener=stream_listener, tweet_mode='extended')

stream.filter(locations = ColoradoGeoBox, languages=["en"])
















