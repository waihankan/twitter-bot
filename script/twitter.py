#!/usr/bin/env python3
import tweepy
import re
import os
import sys
import config

class Twitter():
    def __init__(self, config, tweets_num, username, retweet_only):
        self.config = config
        self.like_counter = 0
        self.retweet_counter = 0
        self.retweet_only = retweet_only
        self.tweets_num = tweets_num
        self.username = username

        if self.checkAuth():
            self.process_tweet()
            
    def checkAuth(self):
        auth = tweepy.OAuthHandler(self.config.api_key, self.config.api_secret)
        auth.set_access_token(self.config.access_token,self.config.token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True)

        if self.api.verify_credentials():
            print("Valid Credentials")
            return True
        else:
            print("Invalid Credentials")
            sys.exit(1)

    def is_retweet(self, tweet):
        pattern=r"^RT @(.*):"
        if re.match(pattern, tweet.text) is not None:
            return True
        else:
            return False

    def like_and_retweet(self, tweet):
        if not tweet.favorited:
            #tweet.favorite()
            self.like_counter += 1
            print("like tweet")
        else:
            print("already liked")

        if not tweet.retweeted:
            # tweet.retweet()
            self.retweet_counter += 1
            print("retweet")
        else:
            print("retweeted post")

    def process_tweet(self):
        self.user = self.api.get_user(self.username)
        self.timeline = self.api.user_timeline(self.username, count=self.tweets_num)

        for tweet in self.timeline:
            if self.retweet_only:
                if self.is_retweet(tweet):
                    self.like_and_retweet(tweet)

            else:
                self.like_and_retweet(tweet)

        print("All good. Like {like} tweets; Retweet {retweet} tweets."
        	.format(like=self.like_counter, retweet=self.retweet_counter))


