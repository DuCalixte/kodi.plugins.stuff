# os and lib modules
import os
import sys
import re
import string
import urllib
import urllib2

# xbmc modules
import xbmc
import xbmcplugin
import xbmcgui
import xbmcaddon

# print_exc
from traceback import print_exc
from resources.lib.scrapper import YoutubeResource

#---------------------------------------------------------------------
__addonID__ = "plugin.video.haiti.metro.news"
__addon__ = xbmcaddon.Addon(__addonID__)
__addonDir__ = __addon__.getAddonInfo("path")
__author__ = __addon__.getAddonInfo("author")
__date__ = "04-21-2017"
__language__ = __addon__.getLocalizedString
__version__ = __addon__.getAddonInfo("version")
#---------------------------------------------------------------------
# Global Variables
ICON_PATH     = os.path.join(__addonDir__,"icon.png")
FANART_PATH   = os.path.join(__addonDir__,"fanart.jpg")

YOUTUBE_CHANNEL_ID = "UU8rH_LswworcG_PAQGJE6jw"
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/user/pluralsight/videos"
YOUTUBE_QUERY_URL = "https://www.googleapis.com/youtube/v3/search?"
YOUTUBE_PLUGIN = "plugin://plugin.video.youtube/?action=play_video&videoid=%s"
YOUTUBE_API_PART = "snippet"
YOUTUBE_API_KEY = "AIzaSyAwIUcZC2onxybXIsow6Wc4rVQdnUaSi1U"
YOUTUBE_PLAYLIST_ID = "UU8rH_LswworcG_PAQGJE6jw"
YOUTUBE_PLAYLIST_FIELDS = "items,nextPageToken,prevPageToken,tokenPagination"
YOUTUBE_SORT_BY_DATE = "date"
YOUTUBE_SORT_BY_DATE_PUBLISHED = "published"
YOUTUBE_SORT_BY_RATING = "rating"
YOUTUBE_SORT_BY_RELEVANCE = "relevance"

class MetroNews:
    """
    main class
    """
    def __init__(self, *args, **kwargs):
        self.set_debug_mode()
        self.youtube = YoutubeResource()
        self.params = self.get_params()
        self.mode = None
        self.url = None
        self.icon_image = ''
        self.name = None
        self.__initialize()
        self.__display_on_mode_change()

        if self.debug_mode:
            xbmc.log("Haiti MetroNews version - %s"%__version__, xbmc.LOGNOTICE)
            # xbmc.log("Haiti MetroNews addon : Python version -> %s"%str(sys.version_info), xbmc.LOGNOTICE)
            # xbmc.log("Haiti MetroNews addon : Addon dir      -> %s"%__addonDir__, xbmc.LOGNOTICE)
            xbmc.log("Haiti MetroNews addon : Mode           -> %s"%str(self.mode), xbmc.LOGNOTICE)
            xbmc.log("Haiti MetroNews addon : URL            -> %s"%str(self.url), xbmc.LOGNOTICE)
            xbmc.log("Haiti MetroNews addon : Name           -> %s"%str(self.name), xbmc.LOGNOTICE)
            xbmc.log("Haiti MetroNews addon : Iconimage      -> %s"%str(self.icon_image), xbmc.LOGNOTICE)

    def show_contents(self):
        response = urllib2('https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.playlistItems.list?part=snippet&maxResults=25&playlistId=UU8rH_LswworcG_PAQGJE6jw&_h=9&')
        tree = json.loads(response.read())
        feed = tree['feed']
    def display_all_categories(self):
        categories = ['Latest videos', 'Le Point', 'Metro News', 'All videos']
        index = 1
        for category in categories:
            self.add_item(category.encode('utf-8'), 'category', index)
            index += 1
    def get_latest_videos(self):
        self.__display_videos(self.__load_videos())
    def get_all_videos(self):
        self.__display_videos(self.__load_videos_with_page_token(50))
    def query_all_videos(self, query, next_mode):
        self.__display_videos_from_query(self.__query_videos_with_page_token(query, 50, next_mode))
    def iterate_all_videos(self):
        self.__display_videos(self.__load_videos_with_page_token(50, self.url))
    def iterate_all_videos_from_query(self, query, next_mode):
        self.__display_videos_from_query(self.__query_videos_with_page_token(query, 50, next_mode, self.url))
    def display_nothing(self):
        addon_name = __addon__.getAddonInfo('name')
        xbmcgui.Dialog().ok(addon_name, "The video source is not playable")
        return None
    def add_item(self,name,url,mode,iconimage="DefaultFolder.png",info={},fanart=FANART_PATH,isPlayable=False):
        _url   = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&iconImage="+urllib.quote_plus(iconimage)
        _item = xbmcgui.ListItem(name, iconImage=iconimage, thumbnailImage=iconimage)
        _item.setInfo(type="Video",infoLabels=info)
        _item.setProperty("Fanart_Image",fanart)
        isFolder = True
        if isPlayable :
            _item.setProperty('IsPlayable','true')
            isFolder = False
        if self.debug_mode:
            xbmc.log("XBMC URL - %s"%_url, xbmc.LOGNOTICE)
            xbmc.log("XBMC DATA - %s"%_item, xbmc.LOGNOTICE)
        return xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=_url,listitem=_item,isFolder=isFolder)
    def get_params(self):
        param  = {}
        params = sys.argv[2]
        if len(params) >= 2 :
            if (params[len(params)-1]=='/'):
                params=params[0:len(params)-2]
            cleanedparams = params.replace('?','')
            pairsofparams = cleanedparams.split('&')
            for i in range(len(pairsofparams)):
                splitparams={}
                splitparams=pairsofparams[i].split('=')
                if (len(splitparams))==2:
                    param[splitparams[0]]=splitparams[1]
        return param
    def play_video(self):
        video_url = YOUTUBE_PLUGIN%self.url
        item = xbmcgui.ListItem(path=video_url)
        xbmcplugin.setResolvedUrl(handle=int(sys.argv[1]), succeeded=True, listitem=item)
    def set_debug_mode(self):
        self.debug_mode = False
        if __addon__.getSetting('debug') == 'true':
            self.debug_mode = True
        print "MetroNews addon: debug mode: %s"%self.debug_mode
    def __initialize(self):
        try:
            self.url=urllib.unquote_plus(self.params["url"])
        except:
            pass
        try:
            self.name=urllib.unquote_plus(self.params["name"])
        except:
            pass
        try:
            self.mode=int(self.params["mode"])
        except:
            pass
        try:
            self.icon_image=urllib.unquote_plus(self.params["iconImage"])
        except:
            pass
    def __display_videos(self, videos):
        for video in videos:
            title = video['snippet']['title']
            url = video['snippet']['resourceId']['videoId']
            try:
                icon_image = video['snippet']['thumbnails']['standard']['url']
            except:
                icon_image = video['snippet']['thumbnails']['default']['url']
            info = {}
            self.add_item(title.encode('utf-8'),url.encode("utf-8"),100,icon_image.encode("utf-8"),info,FANART_PATH, True)
    def __display_videos_from_query(self, items):
        videos = sorted(items, key=lambda k: k['snippet'].get('publishedAt', ""), reverse=True)
        for video in videos:
            try:
                title = video['snippet']['title']
                url = video['id']['videoId']
                try:
                    icon_image = video['snippet']['thumbnails']['high']['url']
                except:
                    icon_image = video['snippet']['thumbnails']['default']['url']
                info = {}
                self.add_item(title.encode('utf-8'),url.encode("utf-8"),100,icon_image.encode("utf-8"),info,FANART_PATH, True)
            except:
                pass
    def __load_videos(self, maxResults = 10):
        params = {'part': YOUTUBE_API_PART, 'maxResults': maxResults, 'playlistId': YOUTUBE_PLAYLIST_ID, 'fields': YOUTUBE_PLAYLIST_FIELDS, 'key': YOUTUBE_API_KEY}
        return self.youtube.load_playlist_items(params)
    def __load_videos_with_page_token(self, maxResults, token = None):
        params = {'part': YOUTUBE_API_PART, 'maxResults': maxResults, 'playlistId': YOUTUBE_PLAYLIST_ID, 'fields': YOUTUBE_PLAYLIST_FIELDS, 'key': YOUTUBE_API_KEY}
        if token:
            params['pageToken'] = token
        response = self.youtube.load_playlist_items_with_tokens(params)
        if 'prevPageToken' in response:
            self.__display_next_prev('Previous', response['prevPageToken'])
        if 'nextPageToken' in response:
            self.__display_next_prev('Next', response['nextPageToken'])
        return response['items']
    def __query_videos_with_page_token(self, query, maxResults, next_mode, token = None):
        params = {'part': YOUTUBE_API_PART, 'q': query, 'maxResults': maxResults, 'playlistId': YOUTUBE_PLAYLIST_ID, 'order': YOUTUBE_SORT_BY_RELEVANCE, 'fields': YOUTUBE_PLAYLIST_FIELDS, 'key': YOUTUBE_API_KEY}
        if token:
            params['pageToken'] = token
        response = self.youtube.query_playlist_items_with_tokens(params)
        if 'prevPageToken' in response:
            self.__display_next_prev_with_query('Previous', next_mode, response['prevPageToken'])
        if 'nextPageToken' in response:
            self.__display_next_prev_with_query('Next', next_mode, response['nextPageToken'])
        return response['items']
    def __display_next_prev(self,title, token):
        self.add_item(title.encode('utf-8'),token.encode("utf-8"), 10)
    def __display_next_prev_with_query(self,title, next_mode, token):
        self.add_item(title.encode('utf-8'),token.encode("utf-8"), next_mode)
    def __display_on_mode_change(self):
        if self.mode is None:
            self.display_all_categories()
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif self.mode==1 :
            self.get_latest_videos()
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif self.mode==2 :
            self.query_all_videos('LE POINT', 20)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif self.mode==3 :
            self.query_all_videos('METRONEWS', 30)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif self.mode==4 :
            self.get_all_videos()
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif self.mode==10 :
            self.iterate_all_videos()
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif self.mode==20 :
            self.iterate_all_videos_from_query('LE POINT', 20)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif self.mode==30 :
            self.iterate_all_videos_from_query('METRONEWS', 30)
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif self.mode==100 :
            self.play_video()
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
        else:
            self.display_nothing()
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
##########################################################################
# BEGIN !
##########################################################################

if (__name__ == "__main__"):
    try:
        MetroNews()
    except:
        print_exc()
