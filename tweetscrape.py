import snscrape.modules.twitter as sntwitter
import random

def randomtweet(handle_name, no_of_tweets):
    tweets_list = []
    paramscraper = f"from:{handle_name} exclude:replies"                
    for i,tweet in enumerate(sntwitter.TwitterSearchScraper(paramscraper).get_items()):
        if i>8:
            break
        tweets_list.append({"url":tweet.url,"user_handle":tweet.user.username,"content":tweet.content,"likes":tweet.likeCount,"date":tweet.date})
    
    tweets = []
    tweets += [ tweets_list[random.randint(0,8)] for i in range(no_of_tweets)  ]
    return tweets

def tweetfeed(tweets_dict,focusmode):
    handles_string = tweets_dict[focusmode]
    handles_list = list(handles_string.split(','))
    collation_list = []
    for handle in handles_list:
        collation_list.extend(randomtweet(handle,random.randint(3,5)))
    random.shuffle(collation_list)
    return collation_list[:5]


# Checks if the twitter handle exists and contains atleast a minimum of 10 tweets.
def checkvalidandviablehandle(handle_name):
    paramscraper = 'from:'+str(handle_name)
    flag = False
    for i in enumerate(sntwitter.TwitterSearchScraper(paramscraper).get_items()):
        if i[0]>10:
            flag = True
            break
    return flag

def checkvalidall(handles):
    flag = True
    handles_list = list(handles.split(','))
    for handle in handles_list:
        if checkvalidandviablehandle(handle) == False:
            flag = False
            break
    return flag
        

