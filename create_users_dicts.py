import re
import pickle
import numpy as np
from pymongo import MongoClient


# Check if the given tweet is from the given social network
def is_from_social_network(tweet, social_network):
    reg_source = re.compile(r"href=.*({}|{}).*>".format(social_network, social_network.capitalize()))
    if reg_source.search(tweet["source"]):
        return True
    else:
        reg_entity = re.compile(r'{}|{}'.format(social_network, social_network.capitalize()))
        for _json in tweet["entities"]["urls"]:
            if reg_entity.search(str(_json)):
                return True
        return False


MONGOHOST = "mongodb://localhost:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&3t.uriVersion=3&3t.connection.name=twitterdb"

client = MongoClient(MONGOHOST)
db = client.twitterdb
collection = db.social_tweets

# Init users dict - one for each social network
instagram_users = {}
facebook_users = {}
pinterest_users = {}
tumblr_users = {}

# users with no match to social network
general_users = set()

# Iterate over all tweets
i = 0
for tweet in collection.find():
    i += 1
    user = tweet['user']['id']
    if is_from_social_network(tweet, 'instagram'):
        if user in instagram_users:
            instagram_users[user] += 1
        else:
            instagram_users[user] = 1

    elif is_from_social_network(tweet, 'facebook'):
        if user in facebook_users:
            facebook_users[user] += 1
        else:
            facebook_users[user] = 1

    elif is_from_social_network(tweet, 'pinterest'):
        if user in pinterest_users:
            pinterest_users[user] += 1
        else:
            pinterest_users[user] = 1

    elif is_from_social_network(tweet, 'tumblr'):
        if user in tumblr_users:
            tumblr_users[user] += 1
        else:
            tumblr_users[user] = 1

    else:
        general_users.add(user)

    if i % 10000 == 0:
        print("Finished {} tweets...".format(i))


print('Num of users with no social network: {}'.format(len(general_users)))

print("################### Instegram ###################")
print('Num of users : %.d' % (len(instagram_users.keys())))
print('Avg Num of tweets per user : %.4f' % (np.mean(list(instagram_users.values()))))
print()

print("################### Facebook ###################")
print('Num of users : %.4f' % (len(facebook_users.keys())))
print('Avg Num of tweets per user : %.4f' % (np.mean(list(facebook_users.values()))))
print()

print("################### Pinterest ###################")
print('Num of users : %.4f' % (len(pinterest_users.keys())))
print('Avg Num of tweets per user : %.4f' % (np.mean(list(pinterest_users.values()))))
print()

print("################### Tumblr ###################")
print('Num of users : %.4f' % (len(tumblr_users.keys())))
print('Avg Num of tweets per user : %.4f' % (np.mean(list(tumblr_users.values()))))
print()


# Save the users dicts
with open('./users_dicts/instagram_users.pkl', mode='wb') as f:
    pickle.dump(instagram_users, f)

with open('./users_dicts/facebook_users.pkl', mode='wb') as f:
    pickle.dump(facebook_users, f)

with open('./users_dicts/pinterest_users.pkl', mode='wb') as f:
    pickle.dump(pinterest_users, f)

with open('./users_dicts/tumblr_users.pkl', mode='wb') as f:
    pickle.dump(tumblr_users, f)

with open('./users_dicts/general_users.pkl', mode='wb') as f:
    pickle.dump(general_users, f)
