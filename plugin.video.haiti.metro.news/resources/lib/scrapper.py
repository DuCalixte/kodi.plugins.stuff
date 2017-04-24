import os
import sys
import requests

YOUTUBE_CHANNEL_URL="https://www.googleapis.com/youtube/v3/channels"
YOUTUBE_PLAYLIST_ITEMS_URL="https://www.googleapis.com/youtube/v3/playlistItems"

class YoutubeResource:
    def __init__(self, *args, **kwargs):
        print "Loading youtube resources"

    def load_channel(self, params):
        return self.__load_contents(YOUTUBE_CHANNEL_URL, params)["items"]

    def load_playlist_items(self, params):
        return self.__load_contents(YOUTUBE_PLAYLIST_ITEMS_URL, params)["items"]

    def __load_contents(self, url, params):
        response = None
        try:
            response = requests.get(url, params)
            return response.json()
        except (RuntimeError, TypeError, NameError, ValueError) as err:
            print("Generic error: {0}".format(err))
            raise
        except OSError as err:
            print("OS error: {0}".format(err))
            raise
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise
