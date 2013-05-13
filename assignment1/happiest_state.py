#!/usr/bin/python
import sys
import json
import re

"""
Class Tweet which will hold the Tweet info.
At present there are two elenemts created_at 
and text. In future planning to add user id
retweeted count, etc for further analysis
"""
class Tweet(object):
	def __init__(self,created_at,text,id_str,location):
		self.created_at = created_at
		self.text = text
		self.id_str = id_str
		self.location = location

"""
TweetSentiment is a class for this assignment
where we will be working on sentiments
"""
class TweetSentiment(Tweet):
	sentiment = 0
	def __init__(self,created_at,text,id_str,location,sentiment = 0):
		Tweet.__init__(self,created_at,text,id_str,location)

class TweetLoader(object):
	"""
	This function will load Tweets from the json
	file
	"""
	tweet_s_list = []
	def load(self,file_name):
		f = open(file_name)
		for line in f:
			json_data = json.loads(line)
			if "delete" not in json_data:		
				#skip all tweets in different language
				if "lang" in json_data:
					if json_data["lang"] != "en":
						continue	
				location = ""
				if 'place' in json_data and json_data['place'] != None:
					location = json_data['place']['full_name']
				else:
					if 'user' in json_data and 'location' in json_data['user'] and json_data['user']['location'] != None:
						location = json_data['user']['location']
					else:
						if 'coordinates' in json_data and json_data['coordinates'] != None: 
							print "coordinates: " + str( json_data['coordinates'] )
							location = str( json_data['coordinates'] )
				if location != "":
					state = getStateFromLocation(location)
					if isinstance( state, basestring ):						
						#throw away the tweets without location info for this problem
						self.tweet_s_list.append( TweetSentiment(json_data['created_at'],json_data['text'],json_data['id_str'],state))
				#print "text = " + json_data["text"]

		return self.tweet_s_list

StateAbbr  = {
	'Alabama':'AL',
	'Alaska':'AK',
	'Arizona':'AZ',
	'Arkansas':'AR',
	'California':'CA',
	'Colorado':'CO',
	'Connecticut':'CT',
	'Delaware':'DE',
	'Florida':'FL',
	'Georgia':'GA',
	'Hawaii':'HI',
	'Idaho':'ID',
	'Illinois':'IL',
	'Indiana':'IN',
	'Iowa':'IA',
	'Kansas':'KS',
	'Kentucky':'KY',
	'Louisiana':'LA',
	'Maine':'ME',
	'Maryland':'MD',
	'Massachusetts':'MA',
	'Michigan':'MI',
	'Minnesota':'MN',
	'Mississippi':'MS',
	'Missouri':'MO',
	'Montana':'MT',
	'Nebraska':'NE',
	'Nevada':'NV',
	'New Hampshire':'NH',
	'New Jersey':'NJ',
	'New Mexico':'NM',
	'New York':'NY',
	'North Carolina':'NC',
	'North Dakota':'ND',
	'Ohio':'OH',
	'Oklahoma':'OK',
	'Oregon':'OR',
	'Pennsylvania':'PA',
	'Rhode Island':'RI',
	'South Carolina':'SC',
	'South Dakota':'SD',
	'Tennessee':'TN',
	'Texas':'TX',
	'Utah':'UT',
	'Vermont':'VT',
	'Virginia':'VA',
	'Washington':'WA',
	'West Virginia':'WV',
	'Wisconsin':'WI',
	'Wyoming':'WY',
	'American Samoa':'AS',
	'District of Columbia':'DC',
	'Federated States of Micronesia':'FM',
	'Guam':'GU',
	'Marshall Islands':'MH',
	'Northern Mariana Islands':'MP',
	'Palau':'PW',
	'Puerto Rico':'PR',
	'Virgin Islands':'VI',
	'Armed Forces Africa':'AE',
	'Armed Forces Americas':'AA',
	'Armed Forces Canada':'AE',
	'Armed Forces Europe':'AE',
	'Armed Forces Middle East':'AE',
	'Armed Forces Pacific':'AP',
	}

def getStateFromLocation(location):
	"""
	search=re.compile(r'(^[\w\s]+,\s\w{2}$)|(^[\w\s]+,\s\w{2}\s\d{5}$)|').search
	if bool(search(location)):		
		#cty, state = location.split(",")
		return state
		"""
	if ',' in location:
		cs = location.split(",")
		state = cs[1].strip()
		if state in StateAbbr.values():
			return state
		elif state in StateAbbr:
			return StateAbbr[state]
	elif location.strip() in StateAbbr.keys():
		return StateAbbr[location.strip()]
	elif location.strip in StateAbbr.values():
		return location.strip()

def loadtweets(file_name):
	loader = TweetLoader()
	return loader.load(file_name)
	
def loadSentimentDB(file_name):
	afinnfile = open(file_name)
	scores = {} # initialize an empty dictionary
	for line in afinnfile:
		term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
		scores[term] = int(score)  # Convert the score to an integer.

	return scores	

def calcSenti(tweets,sentiments):
	#calculate sentiments for each tweet we have
    for tweet in tweets:
    	tweettext = tweet.text;
    	tweetwords = tweettext.split()
    	for tw_word in tweetwords:
    		#print tw_word
    		word = tw_word.lower()
    		if  word in sentiments:
    			tweet.sentiment += sentiments[word]    
    return tweets

def main():
    sent_file 	= sys.argv[1]
    tweet_file 	= sys.argv[2]
    sentiments 	= loadSentimentDB(sent_file)
    tweets 		= loadtweets(tweet_file)

    tweets = calcSenti(tweets,sentiments)

    #now create the dict of tweet vs sentiments
    stateSenti = {}
    stateCount = {}
    for tweet in tweets:
    	if tweet.location not in stateSenti:
    		stateSenti[tweet.location] = 0.0
    	stateSenti[tweet.location] += tweet.sentiment
    	if tweet.location not in stateCount:
    		stateCount[tweet.location] = 0.0
    	stateCount[tweet.location] += 1.0
    
    stateHappyness = {}
    for state in stateSenti:
    	stateHappyness[state] = stateSenti[state]/stateCount[state]
    	
    happyV = max(stateHappyness.values())
    for state in stateHappyness:
    	if stateHappyness[state] == happyV:
    		print state
    		break

if __name__ == '__main__':
    main()
