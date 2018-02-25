import tweepy
import dataset
import os
import json
from html.parser import HTMLParser
database = dataset.connect("sqlite:///tweets.db")
table = database["tweets"]
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

#List of cities to check against status.user.location
cities = ["Denver", "Colorado Springs", "Aurora", "Fort Collins", "Lakewood", "Thorton", "Pueblo", "Arvada", "Westminster", "Centennial", "Boulder"]

class StreamListener(tweepy.StreamListener):
	
	def on_status(self, status):
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
                            tweet=jsono["extended_tweet"]["full_text"]
                            tweet=process(tweet)
                            score=scorer(tweet)
                            if score>0:
                                print("Evaluation: Positive")
                            else:
                                print("Evaluation: Negative")
							print("")
						else:
							print("Said: ",jsono["text"])
                            tweet=jsono["text"]
                            tweet=process(tweet)
                            score=scorer(tweet)
                            if score>0:
                                print("Evaluation: Positive")
                            else:
                                print("Evaluation: Negative")
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
