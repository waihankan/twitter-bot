#!/usr/bin/env python3

import time
import tweepy
import tkinter as tk

auth = tweepy.OAuthHandler("bbI8Zu5WBmAfyqvAKFkMDQbAx", "YCwI8S6bY3jrsfke3MAcBSKO1Dr8OFengEroLvvMNkMnPD5JJX")

auth.set_access_token("1356590402992623619-4DMgFemZEAbLOx52rF7h8CTjVWhw0q",
                      "j6291l2btbERyZxaa7Q8SwiooRRtr4rJ20OoA44kA9dTJ")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

username = input("Enter the screen name of a person you want to retweet the timeline from: ")
number_of_tweets = input("Enter the number of tweets: ")

print("Username: " + username)
print("No.of tweets: " + number_of_tweets + "\n")

print(" _________________________")
print("|                         |")
print("| Starting Retweet + Like |")
print("|                         |")
print(" ------------------------- ")

user = api.get_user(username)
timeline = api.user_timeline(username, count=number_of_tweets)
num = 1

for tweet in timeline:

    try:
        print("\n\nTweet: " + str(num))
        print("______________")
        print(tweet.text)
        print(tweet.user.screen_name)
        print("______________")
        num += 1

        if not tweet.favorited:
            tweet.favorite()
            print("Like tweet")

        else:
            print("Post already liked")

        if not tweet.retweeted:
            tweet.retweet()
            print("Retweet")

        else:
            print("Post already retweet")
            
        time.sleep(5)

    except tweepy.TweepError as e:
        print(e.reason)
        
    except StopIteration:
        break

