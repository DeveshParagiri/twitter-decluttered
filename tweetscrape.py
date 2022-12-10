import snscrape.modules.twitter as sntwitter
import random


def randomtweet(handle_name, no_of_tweets):
    tweets_list = []
    paramscraper = 'from:'+str(handle_name)
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(paramscraper).get_items()):
        if i>10:
            break
        tweets_list.append(tweet.content)
    
    tweets = []
    tweets += [ tweets_list[random.randint(0,10)] for i in range(no_of_tweets)  ]
    return tweets
