import dataset
import os
from datafreeze import freeze
import time
import re 
import csv

#dictionary of cities and their tweet values
city_scores = dict()

#parses a csv file of tweets and locations
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
            print("said:", cleaned_tweet, "in", tweetloc)
            score = scorer(cleaned_tweet, tweetloc)
            if (score == 0):
            	print("nuetral")
            elif (score == -1):
            	print("negative")
            else:
            	print("positive")
            print('\n')

#removes punctuation and lowercases a tweet
def process(raw_tweet):
    raw_tweet= re.sub(r'[^\w\s]','',raw_tweet)
    raw_tweet=raw_tweet.lower()
    return raw_tweet

#scores a tweet based on the number of positive and negative words it contains
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

def main(): 
	

	#continuously update the tweets.csv file
	while True:

		
		#delete the old csv file if present
		
		try:
			os.remove("tweets.csv")
		except:
			pass
		
		#dump the database into the csv file
		
		database = dataset.connect("sqlite:///tweets.db")

		result = database["tweets"].all()

		freeze(result, format='csv', filename="tweets.csv")
		

		#analyze each line in the csv file
		csvReader()

		avg_city_scores = {}

		for key, value in city_scores.items():
			avg_city_scores[key] = sum(value)/ float(len(value))
		print("###########################################")
		print(avg_city_scores)
		
		city_scores.clear()
		#erase the database tweets table
		table = database["tweets"]
		table.delete()

		#wait for five minutes, then redo the above code
		time.sleep(30)

    


if __name__ == "__main__":
    main()

