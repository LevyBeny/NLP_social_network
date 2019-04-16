import tweepy
import json
import re
from requests import session


# override tweepy.StreamListener to add logic to on_status
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print(status.text)

    def on_data(self, raw_data):
        tweet_json = json.loads(raw_data)
        r = re.compile(r"href=.*(instagram|pinterest|Instagram|Pinterest).*>")
        test = r.search(tweet_json["source"])
        if not test:
            print(" Tweet was filtered....")
            print(tweet_json["source"]+"\n")
            return True
        with open('fetched_tweets.txt','a') as tf:
            print("Tweet Accepted !")
            print(tweet_json["source"]+"\n")
            tf.write(raw_data)
        return True



CONSUMER_TOKEN ="GO3wNI7lcybeZucegHIuBu3BD"
CONSUMER_SECRET ="tynoLttKAogFbjCLM6JGS32rQ6sYKPdisPtty4IAOXBZVpkn7H"
ACCESS_TOKEN="1107293654291488768-gewQ3G53w0XXlJZRLRu2t0pAvH7EkU"
ACCESS_TOKEN_SECRET="bhnrWLrivotga31WEphF3bPtLhqmVQIHP55snHSWxnWmX"

auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# search_results = api.search(q="instagram",lang="en")
my_listener = MyStreamListener(api=api)
stream = tweepy.Stream(auth=api.auth, listener=my_listener)
stream.filter(track=["pinterest"],languages=["en"])



# for result in search_results:
#     print(len(search_results))
#     print("User:")
#     print(result.user.name)
#     print("Source:")
#     print(result.source)
#     print("Text:")
#     print(result.text)
#     print("Entities:")
#     print(result.entities['urls'])
#     print("****\n\n*****")
