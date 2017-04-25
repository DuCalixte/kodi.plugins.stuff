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

# YOUTUBE_CHANNEL_URL = "https://www.youtube.com/channel/UC8rH_LswworcG_PAQGJE6jw"
YOUTUBE_CHANNEL_ID = "UU8rH_LswworcG_PAQGJE6jw"
YOUTUBE_CHANNEL_URL = "https://www.youtube.com/user/pluralsight/videos"
YOUTUBE_PLUGIN = "plugin://plugin.video.youtube/?action=play_video&videoid=%s"
YOUTUBE_API_PART = "snippet"
YOUTUBE_API_KEY = "AIzaSyAwIUcZC2onxybXIsow6Wc4rVQdnUaSi1U"
YOUTUBE_PLAYLIST_ID = "UU8rH_LswworcG_PAQGJE6jw"

class MetroNews:
    """
    main class
    """
    def __init__(self, *args, **kwargs):
        self.set_debug_mode()
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
        categories = ['Latest videos', 'All videos']
        index = 1
        for category in categories:
            self.add_item(category.encode('utf-8'), 'category', index)
            index += 1
    def get_latest_videos(self):
        self.__display_videos(self.__load_videos())
    def get_all_videos(self):
        self.__display_videos(self.__load_videos(50))
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
        xbmc.log("XBMC URL - %s"%_url, xbmc.LOGNOTICE)
        xbmc.log("XBMC DATA - %s"%_url, xbmc.LOGNOTICE)
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
            url = video['snippet']['videoId']
            icon_image = video['snippet']['thumbnails']['standard']['url']
            info = video['snippet']
            self.add_item(title,url,3,icon_image,info,FANART_PATH, True):
    def __load_videos(self, maxResults = 10):
        params = {'part': YOUTUBE_API_PART, 'maxResults': maxResults, 'playlistId': YOUTUBE_PLAYLIST_ID, 'key': YOUTUBE_API_KEY}
        return self.list.load_playlist_items(params)
    def __display_on_mode_change(self):
        if self.mode is None:
            self.display_all_categories()
            xbmcplugin.endOfDirectory(int(sys.argv[1]))
         elif self.mode==1 :
             self.get_latest_videos()
             xbmcplugin.endOfDirectory(int(sys.argv[1]))
        elif self.mode==2 :
            self.get_all_videos()
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
