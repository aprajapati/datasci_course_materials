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
	def __init__(self,created_at,text,id_str):
		self.created_at = created_at
		self.text = text
		self.id_str = id_str

"""
TweetSentiment is a class for this assignment
where we will be working on sentiments
"""
class TweetSentiment(Tweet):
	sentiment = 0
	def __init__(self,created_at,text,id_str,sentiment = 0):
		Tweet.__init__(self,created_at,text,id_str)

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
				self.tweet_s_list.append( TweetSentiment(json_data['created_at'],json_data['text'],json_data['id_str']))
				#print "text = " + json_data["text"]

		return self.tweet_s_list

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

def deriveTweetSentiments( tweets, sentiments ):
	#calculate sentiments for each tweet we have
    for tweet in tweets:
    	tweettext = tweet.text;
    	tweetwords = tweettext.split()
    	for tw_word in tweetwords:
    		word = tw_word.lower()
    		if word in sentiments:
    			tweet.sentiment += sentiments[word]
    return tweets
    
def isATerm(term, search=re.compile(r'^[a-zA-Z]+$').search):
	return bool(search(term))

def isIgnore(term):
	ignoreList = ['a', 'the', 'these', 'those', 'that', 'this', 'an', 'rt', 'he', 'she', 'it', 'is', 'are', 'i', 'they', 'you']
	if term.lower() in ignoreList:
		return True
	
class Terms(object):
	nTotalCount = 0
	nTotalSenti = 0.0
	sentiment = 0.0 
		
def main():
    sent_file 	= sys.argv[1]
    tweet_file 	= sys.argv[2]
    sentiments 	= loadSentimentDB(sent_file)
    tweets 		= loadtweets(tweet_file)
    terms = {}

    #calculate sentiments for each tweet we have
    tweets = deriveTweetSentiments(tweets, sentiments)
    
    for tweet in tweets:
    	tweettext = tweet.text;
    	tweetwords = tweettext.split()
    	for tw_word in tweetwords:
    		tw_word = tw_word.lower()
    		if tw_word not in sentiments:
    		 	if isATerm(tw_word) and not isIgnore(tw_word):
    			  	if tw_word not in terms.keys():
    			  		terms[tw_word] = Terms()
    			  	if tweet.sentiment > 0:
    			  		terms[tw_word].nTotalSenti += 1
    			  	elif tweet.sentiment < 0:
    			  		terms[tw_word].nTotalSenti -= 1
    			  	terms[tw_word].nTotalCount += 1   	
    for term in terms.keys():
    	terms[term].sentiment = terms[term].nTotalSenti / terms[term].nTotalCount
    	print term + " " + str( terms[term].sentiment )
    

if __name__ == '__main__':
    main()
