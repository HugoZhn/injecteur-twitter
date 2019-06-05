import tweepy
from utils import get_from_env


class TwitterConnector:

    def __init__(self):
        auth = tweepy.OAuthHandler(get_from_env("TWITTER_CONSUMER_KEY"), get_from_env("TWITTER_CONSUMER_SECRET"))
        auth.set_access_token(get_from_env("TWITTER_ACCESS_TOKEN_KEY"), get_from_env("TWITTER_ACCESS_TOKEN_SECRET"))

        stream_listener = CustomStreamListener()
        self.stream = tweepy.Stream(auth=auth, listener=stream_listener)

    def start_stream(self, follow=None, track=None):
        follow = [follow, ] if (type(follow) == str) else follow
        track = [track, ] if (type(track) == str) else track

        if follow and track:
            self.stream.filter(follow=follow, track=track, languages=["fr"])
        elif follow:
            self.stream.filter(follow=follow, languages=["fr"])
        elif track:
            self.stream.filter(track=track, languages=["fr"])


class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        # -- TO DO--
        print(status.text)
        pass
