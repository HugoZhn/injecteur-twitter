import tweepy
from confluent_kafka import Producer
from utils import get_from_env
import json
import time


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
        self.topic_name = get_from_env("TOPIC_NAME")
        print("Gonna produce in ", self.topic_name)
        self.producer = Producer({'bootstrap.servers': 'localhost:9092'})

    def on_status(self, status):
        try:
            self.producer.produce(self.topic_name, json.dumps(status._json))
        except BufferError as buff_err:
            print(buff_err)
            print("Going to pause for 15 seconds")
            time.sleep(15)
            print("Here we go again")
            self.producer.produce(self.topic_name, json.dumps(status._json))
        print("Producing")

    def on_warning(self, notice):
        print(notice)

    def on_disconnect(self, notice):
        print(notice)
        print("DISCONECTED")

    def on_timeout(self):
        print("TIMEOUT")

    def on_error(self, status_code):
        print(status_code)
        if status_code == 420:
            time.sleep(120)
            return True
