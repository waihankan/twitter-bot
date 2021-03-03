#!/usr/bin/env python3
import tweepy
import re
import os
import sys
import config
import emoji

class Twitter():
    def __init__(self, config, tweets_num, username, retweet_only):
        self.config = config
        self.like_counter = 0
        self.retweet_counter = 0
        self.retweet_only = retweet_only
        self.tweets_num = tweets_num
        self.username = username
        self.log = []
        
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

    def _is_retweet(self, tweet):
        pattern=r"^RT @(.*):"
        if re.match(pattern, tweet.text) is not None:
            return True
        else:
            return False

    def _like_and_retweet(self, tweet):
        if not tweet.favorited:
            tweet.favorite()
            self.like_counter += 1
            print("like tweet")
        else:
            print("already liked")

        if not tweet.retweeted:
            tweet.retweet()
            content = "* " +tweet.text[:45].replace('\n', ' ')
            content = content.replace('RT @', '')
            self.log.append(content)
            self.retweet_counter += 1
            print("retweet")
        else:
            content = "# " +tweet.text[4:46].replace('\n', ' ')
            self.log.append(content)
            print("retweeted post")


    def process_tweet(self):
        self.user = self.api.get_user(self.username)
        self.timeline = self.api.user_timeline(self.username, count=self.tweets_num)
        self.sname = self.user.screen_name

        for tweet in self.timeline:
            if self.retweet_only:
                if self._is_retweet(tweet):
                    self._like_and_retweet(tweet)

            else:
                self._like_and_retweet(tweet)

        print("All good. Like {like} tweets; Retweet {retweet} tweets."
        	.format(like=self.like_counter, retweet=self.retweet_counter))

        self.log.append(">> Successfully Like {like} tweets; Retweet {retweet} tweets.\n"
        	.format(like=self.like_counter, retweet=self.retweet_counter))

    def get_log(self):
    	return self.log

    def user_screen(self):
    	return self.sname



