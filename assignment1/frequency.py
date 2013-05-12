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
                self.tweet_s_list.append( Tweet(json_data['created_at'],json_data['text'],json_data['id_str']))
                #print "text = " + json_data["text"]

        return self.tweet_s_list

def loadtweets(file_name):
    loader = TweetLoader()
    return loader.load(file_name)
    
def isATerm(term, search=re.compile(r'^[a-zA-Z]+$').search):
    return bool(search(term))

def isIgnore(term):
    ignoreList = ['a', 'the', 'these', 'those', 'that', 'this', 'an', 'rt', 'he', 'she', 'it', 'is', 'are', 'i', 'they', 'you']
    if term.lower() in ignoreList:
        return True
    
class Terms(object):
    nTotalCount = 0.0     
    nTermFreq = 0.0
        
def main():
    tweet_file     = sys.argv[1]
    tweets         = loadtweets(tweet_file)
    terms = {}
    nTotalTerms = 0

    for tweet in tweets:
        tweettext = tweet.text;
        tweetwords = tweettext.split()
        for tw_word in tweetwords:
            tw_word = tw_word.lower()
            if isATerm(tw_word) and not isIgnore(tw_word):
                 if tw_word not in terms.keys():
                     terms[tw_word] = Terms()                 
                 terms[tw_word].nTotalCount += 1
                 nTotalTerms += 1       
    for term in terms.keys():
        terms[term].nTermFreq = terms[term].nTotalCount / nTotalTerms
        print term + " " + str( terms[term].nTermFreq )
    

if __name__ == '__main__':
    main()
