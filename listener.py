import tweepy
import json
import re
import pickle
from pymongo import MongoClient


MONGOHOST = "mongodb://localhost:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&3t.uriVersion=3&3t.connection.name=twitterdb"
social_networks = ["pinterest","facebook","instagram","tumblr"]

# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)


    def create_source_string(self,network):
        reg_source = re.compile(r"href=.*({}|{}).*>".format(network, network.capitalize()))
        return reg_source

    def create_entity_string(self, network):
        reg_entity = re.compile(r'{}|{}'.format(network, network.capitalize()))
        return reg_entity

    def filter_tweets_by_network(self, tweet_json,network):
        reg_source = self.create_source_string(network)
        reg_entity = self.create_entity_string(network)
        result = None
        for _json in tweet_json["entities"]["urls"]:
            if result:
                break
            result = reg_entity.search(str(_json))

        if not result:
            result = reg_source.search(tweet_json["source"])
        return result

    # Implements tweets filtering when data arrives
    def on_data(self, raw_data):
        try:
            client = MongoClient(MONGOHOST)
            db = client.twitterdblinkedin

            tweet_json = json.loads(raw_data)

           # reg_source = re.compile(r"href=.*(instagram|pinterest|Instagram|Pinterest|facebook|Facebook|tumblr|Tumblr).*>")
            #reg_entity = re.compile(r'instagram|pinterest|Instagram|Pinterest|facebook|Facebook|tumblr|Tumblr')

            result = self.filter_tweets_by_network(tweet_json,"linkedin")
            if result:
                print("Tweet Accepted {}".format(tweet_json["source"]))
                db.social_tweets.insert(tweet_json)

        except Exception as e:
            print(e)


# Credentials for twitter API
CONSUMER_TOKEN ="GO3wNI7lcybeZucegHIuBu3BD"
CONSUMER_SECRET ="tynoLttKAogFbjCLM6JGS32rQ6sYKPdisPtty4IAOXBZVpkn7H"
ACCESS_TOKEN="1107293654291488768-gewQ3G53w0XXlJZRLRu2t0pAvH7EkU"
ACCESS_TOKEN_SECRET="bhnrWLrivotga31WEphF3bPtLhqmVQIHP55snHSWxnWmX"

# Twitter Authentication
auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)


# Activate twitter streaming
my_listener = MyStreamListener(api=api)
stream = tweepy.Stream(auth=api.auth, listener=my_listener)
# stream.filter(track=["bag","linkedin"],languages=["en"])

# Load the users dicts
uniques_dict = {}

unique_path = "./unique_dicts/{}.pkl"
users_list = []
for network in social_networks:
    with open(unique_path.format(network), mode='rb') as f:
        uniques_dict[network] = pickle.load(f)
    users_list += list(uniques_dict[network].keys())

stream.filter(follow=users_list)


