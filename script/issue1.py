import config
import tweepy
import sys
import re


# setup twitter API
auth = tweepy.OAuthHandler(config.api_key, config.api_secret)
auth.set_access_token(config.access_token, config.token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

admin = api.me()

url = input("\nWelcome to Twitter Bot CML!\n---------------------------\nURL: ")

# print("Link: " + url)

pattern = r"https:\/\/twitter\.com\/(.+)\/status\/(\d*)"
result = re.findall(pattern, url)

user_id = result[0][0]
tweet_id = result[0][1]
# print(user_id, tweet_id)

api = tweepy.API(auth)

tweet = api.get_status(tweet_id)

if not tweet.favorited:
    tweet.favorite()
    print("-> favorite tweet")

else:
    print("-> tweet already favorited")

if not tweet.retweeted:
    tweet.retweet()
    print("-> retweet tweet")

else:
    print("-> tweet already retweeted")

# print(admin.screen_name)
    
relationships =  api.lookup_friendships(user_ids=(admin.id, user_id))

for relationship in relationships: 
    if not relationship.is_following:
        api.create_friendship(user_id)
        print("-> follow the tweet user")
    else:
        print("-> already followed the user!")
print("Done!")
sys.exit(0)
