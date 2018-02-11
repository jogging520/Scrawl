import tweepy
from tweepy import OAuthHandler

consumer_key = 'lzw6GTWA81NmKhwbxTBwZwuZQ'
consumer_secret = 'wpIqn4SgVh3obpy9I5dL3hmaDO2pqNnkoqP8LF6Sx6iLgSF4IJ'
access_token = '878524041098805249-Vk7Try2mAxqpfxxgFYPt0Y9vNsT6Eqq'
access_secret = 'hP46IeTIIPbUpeRcx2UMkrJoYt6uS0HnFGMW3RlJsA9gW'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)

api = tweepy.API(auth, proxy="127.0.0.1:8118")

#打印我自己主页上的时间轴里的内容
# public_tweets = api.home_timeline()
# for tweet in public_tweets:
#     print(tweet.text)
public_tweets = api.user_timeline('realDonaldTrump',count=20)
i=1;
for tweet in public_tweets:
    print(i,tweet.created_at,tweet.text)
    i = i+1