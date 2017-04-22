# os and lib modules
import os
import sys
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
ICON_PATH = os.path.join(__addonDir__, "icon.png")
FANART_PATH = os.path.join(__addonDir__, "fanart.jpg")

YOUTUBE_CHANEL_URL = "https://www.youtube.com/channel/UC8rH_LswworcG_PAQGJE6jw"
YOUTUBE_PLUGIN = "plugin://plugin.video.youtube/?action=play_video&videoid=%s"


class MetroNews:
    print "hello"

##########################################################################
# BEGIN !
##########################################################################

if (__name__ == "__main__"):
    try:
        MetroNews()
    except:
        print_exc()
