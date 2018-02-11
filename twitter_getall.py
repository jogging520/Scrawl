#!/usr/bin/env python
# encoding: utf-8

import tweepy  # https://github.com/tweepy/tweepy
import csv

# Twitter API credentials
consumer_key = 'lzw6GTWA81NmKhwbxTBwZwuZQ'
consumer_secret = 'wpIqn4SgVh3obpy9I5dL3hmaDO2pqNnkoqP8LF6Sx6iLgSF4IJ'
access_token = '878524041098805249-Vk7Try2mAxqpfxxgFYPt0Y9vNsT6Eqq'
access_secret = 'hP46IeTIIPbUpeRcx2UMkrJoYt6uS0HnFGMW3RlJsA9gW'

def get_all_tweets(screen_name):
    # Twitter only allows access to a users most recent 3240 tweets with this method

    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)
    api = tweepy.API(auth, proxy="127.0.0.1:8118")
    print('getall')
    # initialize a list to hold all the tweepy Tweets
    alltweets = []

    # make initial request for most recent tweets (200 is the maximum allowed count)
    new_tweets = api.user_timeline(screen_name=screen_name, count=200)
    # save most recent tweets
    alltweets.extend(new_tweets)
    # save the id of the oldest tweet less one
    oldest = alltweets[-1].id - 1 # 773539317377478656 773539317377478656

    # keep grabbing tweets until there are no tweets left to grab
    while len(new_tweets) > 0:
        print("getting tweets before %s", oldest)
        try:
            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = api.user_timeline(screen_name=screen_name, count=100, max_id=oldest)
            if not new_tweets :
                print('null')
            # save most recent tweets
            alltweets.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = alltweets[-1].id - 1
        except:
            print('net meets some troble')
            pass

        print("...%s tweets downloaded so far" ,len(alltweets))
    print("have done!")
    # transform the tweepy tweets into a 2D array that will populate the csv
    outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
    # write the csv
    with open('%s_tweets_new.csv' % screen_name, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(["id", "created_at", "text"])
        writer.writerows(outtweets)

    pass


if __name__ == '__main__':
    # pass in the username of the account you want to download
    get_all_tweets("BarackObama")