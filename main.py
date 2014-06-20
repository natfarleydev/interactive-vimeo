
import ConfigParser
import os

Config = ConfigParser.ConfigParser()
# cfgfile = open(os.path.expanduser('~/.interactive-vimeo'), 'w+')
Config.read(os.path.expanduser('~/.interactive-vimeo'))

# Config file should look like
# [Main]
# access_token = a97609a76a876a987a69a87a69a876a987a78a3a
# favourite_channel_uri = 563335

#Set up the credentials
ACCESS_TOKEN = Config.get('Main','access_token')
CLIENT_ID = u'f85c0d19903c40a22e34028cfd02afb2b5b234b7'
CLIENT_SECRET = u'8563c02571bb352fa090968c291cb90a457577c1'

import vimeo

v = vimeo.VimeoClient(ACCESS_TOKEN, CLIENT_ID, CLIENT_SECRET)

favourite_channel = getattr(v.channels,
                            str(Config.get('Main','favourite_channel_uri')))


def allMyVideos():
    """An iteratable list of all my videos."""
    return v.me.videos(per_page=9001)['body']['data']

# TODO fix the page over 9000 thing to the recommended solution
def putAllVideosInChannel():
    """Put all videos in favourite_channel channel (if not already present)."""
    already_in_channel = []
    for channel_video in favourite_channel.videos(per_page=9001)['body']['data']:
        already_in_channel.append(channel_video['uri'].split('/')[-1:][0])
    print already_in_channel

    for i in allMyVideos():
        tmpuri = i['uri'].split('/')[-1:][0]
        if not tmpuri in already_in_channel:
            print "adding " + i['name'] + " to channel."
            favourite_channel.videos.put(tmpuri)

def listOfAllMyVideos():
    """A human readable list of all my videos."""
    for i in allMyVideos():
        print i['uri'].split('/')[-1:][0] + "\t" + i['name']

def renameVideo(video_id,name):
    """Easy way to rename a video."""
    getattr(v.videos, video_id).patch( {'name' : name } )

def capitaliseAllVideos():
    """Easy way to make sure all videos have consistent capitalisation."""
    from titlecase import titlecase
    for i in allMyVideos():
        tmpname = titlecase(i['name'])
        
        # If it's not capitalised correctly, correct it
        if not tmpname == i['name']:
            tmpuri = i['uri'].split('/')[-1:][0]
            renameVideo(tmpuri,tmpname)
            print "Renamed " + tmpname + "."

import re
def geturi(pattern):
    """Get a list of uri's based on a regular expression"""
    match_list = []
    for i in allMyVideos():
        if re.search(pattern,i['name']):
            print i['name'] + ': recording uri: ' + i['uri'].split('/')[-1:][0]
            match_list.append(i['uri'].split('/')[-1:][0])
    return match_list
        

# geturi('(.*[^(in BSL)]$)') matches videos without (in BSL) at the end

def findAndReplace(find_string, replace_string):
    """Simple function to find and replace exact strings in video names."""
    for i in allMyVideos():
        tmpname = i['name']
        tmpname = tmpname.replace(find_string,replace_string)
        print tmpname
        tmpuri = i['uri'].split('/')[-1:][0]
        renameVideo(tmpuri,tmpname)


def removeDotMov():
    """Simple function to remove any '.mov' from names."""
    for i in allMyVideos():
        tmpname = i['name']
        tmpname = tmpname.replace('.mov','')
        print tmpname
        tmpuri = i['uri'].split('/')[-1:][0]
        renameVideo(tmpuri,tmpname)

def addInBSL():
    """Simple function to add '(in BSL)' if not already present."""
    # TODO add an if statement 'if tagged BSLDictionary and not match (in BSL)'
    for i in allMyVideos():
        tmpname = i['name']
        tmpuri = i['uri'].split('/')[-1:][0]
        if not re.search('.*(in BSL)', tmpname):
            print 'Adding \'(in BSL)\' to ' + tmpname
            tmpname = tmpname + ' (in BSL)'
            renameVideo(tmpuri,tmpname)
