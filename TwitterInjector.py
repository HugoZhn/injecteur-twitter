import tweepy
from confluent_kafka import Producer
from utils import get_from_env
import json


class TwitterInjector:

    def __init__(self):

        auth = tweepy.OAuthHandler(get_from_env("TWITTER_CONSUMER_KEY"), get_from_env("TWITTER_CONSUMER_SECRET"))
        auth.set_access_token(get_from_env("TWITTER_ACCESS_TOKEN_KEY"), get_from_env("TWITTER_ACCESS_TOKEN_SECRET"))

        stream_listener = CustomStreamListener()
        self.stream = tweepy.Stream(auth=auth, listener=stream_listener)

    def start_stream(self, follow=None, track=None):
        follow = [follow, ] if (type(follow) == str) else follow
        track = [track, ] if (type(track) == str) else track

        if follow and track:
            self.stream.filter(follow=follow, track=track, languages=["en"])
        elif follow:
            print("**OPENING THE STREAM")
            self.stream.filter(follow=follow, languages=["en"])
        elif track:
            self.stream.filter(track=track, languages=["en"])


class CustomStreamListener(tweepy.StreamListener):

    def __init__(self):
        super().__init__()
        self.producer = Producer({'bootstrap.servers': 'localhost:9092'})

    def on_status(self, status):
        self.producer.produce("tweets", json.dumps(status._json))
        print("Producing")

    def on_warning(self, notice):
        print(notice)

    def on_disconnect(self, notice):
        print(notice)
        print("DISCONECTED")

    def on_timeout(self):
        print("DISCONECTED")

    def on_error(self, status_code):
        print("AAAAAAAAAAAAAAAAAAA")
        if status_code == 420:
            # returning False in on_error disconnects the stream
            return False
