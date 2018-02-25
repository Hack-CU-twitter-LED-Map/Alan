import tweepy
import dataset
import os
import simplejson as json

database = dataset.connect("sqlite:///tweets.db")
table = database["tweets"]


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
						if True:
							print("#############################################################")
							print("testing full text")
							print(jsono)
							print("#############################################################")
						else:
							print(jsono['text'])
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








