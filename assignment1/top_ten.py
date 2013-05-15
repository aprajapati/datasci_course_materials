#!/usr/bin/python
import sys
import json
import operator

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
				if "entities" in json_data:		
					hashtags = json_data['entities']['hashtags']
					for hashtag in hashtags:
						#skip all tweets in different language
						self.tweet_s_list.append( Tweet(json_data['created_at'],hashtag['text'],json_data['id_str']))					
		return self.tweet_s_list

def loadtweets(file_name):
	loader = TweetLoader()
	return loader.load(file_name)
	

def main():
    tweet_file 	= sys.argv[1]
    tweets 		= loadtweets(tweet_file)

    hashtag = {}
     #calculate sentiments for each tweet we have
    for tweet in tweets:
    	tweettext = tweet.text;
    	tweetwords = tweettext.split()
    	for tw_word in tweetwords:
    		if tw_word not in hashtag:
    			hashtag[tw_word] = 0
    		hashtag[tw_word] += 1


    sorted_x = sorted(hashtag.iteritems(), key=operator.itemgetter(1), reverse=True)
    count = 0
    for i in sorted_x:
    	print str(i[0]) + " " + str(i[1])
    	count += 1
    	if count == 10:
    		break

if __name__ == '__main__':
    main()
