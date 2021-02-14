import time
import tweepy

auth = tweepy.OAuthHandler("bbI8Zu5WBmAfyqvAKFkMDQbAx", "YCwI8S6bY3jrsfke3MAcBSKO1Dr8OFengEroLvvMNkMnPD5JJX")
auth.set_access_token("1356590402992623619-4DMgFemZEAbLOx52rF7h8CTjVWhw0q",
                      "j6291l2btbERyZxaa7Q8SwiooRRtr4rJ20OoA44kA9dTJ")

api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

user = api.get_user('yunwaddylm')
print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
    print(friend.screen_name)
