import dataset
import os
from datafreeze import freeze
import time


while True:
	try:
		os.remove("tweets.csv")
	except:
		pass

	database = dataset.connect("sqlite:///tweets.db")

	result = database["tweets"].all()

	freeze(result, format='csv', filename="tweets.csv")

	table = database["tweets"]
	table.delete()

	time.sleep(300.0)