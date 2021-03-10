#!/usr/bin/env python3
import tweepy
import re
import os
import sys
import config
import emoji

class Twitter():
    def __init__(self, config, tweets_num, username, retweet_only, hashtag):
        self.hashtag = hashtag
        self.config = config
        self.like_counter = 0
        self.retweet_counter = 0
        self.retweet_only = retweet_only
        self.tweets_num = tweets_num.replace(' ', '')
        self.username = username.replace(' ', '')
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
        if re.match(pattern, tweet.full_text) is not None:
            return True
        else:
            return False


    def _check_hashtag(self, text):
        pattern = ".*" + self.hashtag + ".*"
        if self.hashtag == '':
            return True

        elif re.match(pattern, text.replace('\n', '').replace('\r', '')) is not None:
            return True
        
        else:
            self.log.append("? Hashtag not match")
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
            content = "* " +tweet.full_text[:48].replace('\n', ' ')
            content = content.replace('RT @', '')
            self.log.append(content)
            self.retweet_counter += 1
            print("retweet")
        else:
            content = "# " +tweet.full_text[4:49].replace('\n', ' ')
            self.log.append(content)
            print("retweeted post")


    def process_tweet(self):
        try:
            self.user = self.api.get_user(self.username)
            if not re.match(r"^\d+$", self.tweets_num):
                self.log.append("Please Enter a valid number of tweets. [1-100]")
                return True
            
            self.timeline = self.api.user_timeline(self.username, count=self.tweets_num
                    ,tweet_mode="extended")
            self.sname = self.user.screen_name

            for tweet in self.timeline:
                if self.retweet_only:
                    if self._is_retweet(tweet) and self._check_hashtag(tweet.full_text):
                        self._like_and_retweet(tweet)

                else:
                    if self._check_hashtag(tweet.full_text):
                        self._like_and_retweet(tweet)

            print("All good. Like {like} tweets; Retweet {retweet} tweets."
                    .format(like=self.like_counter, retweet=self.retweet_counter))

            self.log.append(">> Successfully Like {like} tweets; Retweet {retweet} tweets.\n"
                    .format(like=self.like_counter, retweet=self.retweet_counter))
        
        except tweepy.TweepError as e:
            self.log.append(e.reason)

    def get_log(self):
    	return self.log

    def user_screen(self):
    	return self.sname



