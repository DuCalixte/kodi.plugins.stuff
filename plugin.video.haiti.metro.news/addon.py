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


class MetroNews:
    """
    main class
    """
    def __init__(self, *args, **kwargs):
        print "<==========================>"
        print "Haiti MetroNews version - %s"%__version__
        print "<==========================>"
        self.set_debug_mode()
        self.params = self.get_params()
        self.mode = None
        self.url = None
        self.icon_image = ''
        self.name = None
        self.__initialize()
        self.__display_on_mode_change()
        xbmc.log("Haiti MetroNews version")
        # xbmc.log("Haiti MetroNews addon : Python version -> %s"%str(sys.version_info, xbmc.LOGDEBUG)
        # xbmc.log("Haiti MetroNews addon : Addon dir      -> %s"%__addonDir__, xbmc.LOGDEBUG)
        xbmc.log("Haiti MetroNews addon : Mode           -> %s"%str(self.mode), xbmc.LOGDEBUG)
        xbmc.log("Haiti MetroNews addon : URL            -> %s"%str(self.url), xbmc.LOGDEBUG)
        xbmc.log("Haiti MetroNews addon : Name           -> %s"%str(self.name), xbmc.LOGDEBUG)
        xbmc.log("Haiti MetroNews addon : Iconimage      -> %s"%str(self.icon_image), xbmc.LOGDEBUG)
        if self.debug_mode:
            print "Haiti MetroNews addon : Python version -> %s"%str(sys.version_info
            print "Haiti MetroNews addon : Addon dir      -> %s"%__addonDir__
            print "Haiti MetroNews addon : Mode           -> "+str(self.mode)
            print "Haiti MetroNews addon : URL            -> "+str(self.url)
            print "Haiti MetroNews addon : Name           -> "+str(self.name)
            print "Haiti MetroNews addon : Iconimage      -> "+str(self.icon_image)

    def show_contents(self):
        response = urllib2('https://developers.google.com/apis-explorer/#p/youtube/v3/youtube.playlistItems.list?part=snippet&maxResults=25&playlistId=UU8rH_LswworcG_PAQGJE6jw&_h=9&')
        tree = json.loads(response.read())
        feed = tree['feed']
    def display_all_categories(self):
        categories = ['Latest videos', 'All videos']
        for category in categories:
            self.add_item(category.encode('utf-8'), 'category', 1)
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
        print "url %s"%_url
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
    def __display_on_mode_change(self):
        if self.mode is None:
            self.display_all_categories()
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
