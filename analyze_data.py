import re
from pymongo import MongoClient

MONGOHOST = "mongodb://localhost:27017/?serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&3t.uriVersion=3&3t.connection.name=twitterdb"

# override tweepy.StreamListener to add logic to on_status
class DataExtraction():
    def __init__(self,collection):
        self.collection = collection

    def get_tweets_by_social_network(self,social_network):
        regex = re.compile(r"href=.*({}|{}).*>".format(social_network, social_network.capitalize()))
        regex_str = r"href=.*({}|{}).*>".format(social_network, social_network.capitalize())
        reg_entity = re.compile(r'{}|{}'.format(social_network, social_network.capitalize()))

        regex_str = r"href=.*({}|{}).*>".format(social_network, social_network.capitalize())
        res_source = list(self.collection.find({"source": {'$regex':regex_str}}))
        #res_entity =list(self.collection.find({"source":{"urls":{}} regex}))

       # res_entity =
        return res_source


client = MongoClient(MONGOHOST)
db = client.twitterdb
collection = db.twitter_search

d_extraction = DataExtraction(collection)
pinterest_tweets = d_extraction.get_tweets_by_social_network("pinterest")

print(len(pinterest_tweets))
# print(pinterest_tweets)
