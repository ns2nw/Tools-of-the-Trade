from __future__ import absolute_import, print_function

from tweepy import OAuthHandler, Stream, StreamListener
import json
import pymongo
import sys

# Go to http://apps.twitter.com and create an app.
# The consumer key and secret will be generated for you after
consumer_key="QO3xHxhlF1WML6Lkrt0X50ExY"
consumer_secret="OCEnt2Y0tZYP0S5ViwkZ8d8yMkdAUiCgQqJ8Uq4UPVaorAgnp4"

# After the step above, you will be redirected to your app's page.
# Create an access token under the the "Your access token" section
access_token="3420797693-BqitqZ0ryR6MJDT5BfckIDWOrDmNCVNKLyOO1y6"
access_token_secret="uRnlgrhFHrOc7lOQGPxjB1BSGHBkXMhLCXD4Iph8k4r3L"
hashtag = None

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    conn = None
    db = None
    collection = None

    def __init__(self):
        self.conn = pymongo.MongoClient("mongodb://readwriteuser:icanreadwrite@192.168.1.70:32772/twitter")
        self.db = self.conn['twitter']
        self.collection = self.db['twitter_data']
        print(hashtag)

    def on_data(self, data):
        tweet = json.loads(data)
        isretweeted = tweet.get("retweeted")
        if ( not isretweeted ):
            row = {}
            row["timestamp"] = tweet.get("timestamp_ms")
            tuser = tweet.get("user")
            row["screen_name"] =tuser.get("screen_name")
            row["hashtag"] =hashtag
            self.collection.insert_one(row)
            print(" inserted")
            print("=====================")
            print("")
        return True

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            print("Error 420 Rate limit from API")
            return False
        return True

if __name__ == '__main__':
    argument_array = sys.argv
    if ( len(argument_array) != 2 ):
        print(" usage is: twitter.py hashtag_to_analyze")
        quit()
    hashtag=sys.argv[1]
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = Stream(auth, l)
    stream.filter(track=[hashtag])
