from plexapi.server import PlexServer
from fuzzywuzzy import process
import plexController as px
import pychromecast



class SnipsPlex:

    def __init__(self, baseurl, token):

        self.plex = PlexServer(baseurl, token)

    def setup_cc(self, cast):
        chromecasts = pychromecast.get_chromecasts()
        #match = process.extractOne(cast, sdict.keys())
        ccs = {}
        for cc in chromecasts:
            ccs[cc.device.friendly_name] = cc
        match = process.extractOne(cast, ccs.keys())
        self.cc = ccs[match[0]]
        pxr = px.PlexController()
        self.cc.register_handler(pxr)
        token = self.plex.query('/security/token?type=delegation&scope=all').attrib['token']
        pxr.namespace = 'urn:x-cast:com.google.cast.sse'
        return pxr

    def get_mc(self,cast):
        chromecasts = pychromecast.get_chromecasts()
        # match = process.extractOne(cast, sdict.keys())
        ccs = {}
        for cc in chromecasts:
            ccs[cc.device.friendly_name] = cc
        match = process.extractOne(cast, ccs.keys())
        cc = ccs[match[0]]
        mc = cc.media_controller
        return mc
    def Get_movie_list(self):
        mlist = []
        movies = self.plex.library.section('Movies').all()
        for video in movies:
            mlist.append(video.title)
        return mlist

    def Get_tv_list(self):
        TVlist = []
        TV = self.plex.library.section('TV Shows').all()
        for video in TV:
            TVlist.append(video.title)
        return TVlist

    def List_OnDeck(self):
        dlist = []
        ondeck = self.plex.library.onDeck()
        for show in ondeck:
            dlist.append(show.grandparentTitle)
        return dlist

    def Dict_OnDeck(self):
        ddict = {}
        ondeck = self.plex.library.onDeck()
        for show in ondeck:
            ddict[show.grandparentTitle] = show
        return ddict

    def Dict_Movies(self):
        mdict = {}
        movies = self.plex.library.section ('Movies').all ()
        for movie in movies:
            mdict[movie.title] = movie
        return mdict

    def playTVonDeck(self, show, cast):
        sdict = self.Dict_OnDeck()
        match = process.extractOne(show, sdict.keys())
        ep = sdict[match[0]]
        tv = self.setup_cc(cast)
        tv.play_media(ep, self.plex)

    def play_movie(self, movie , cast):
        mdict = self.Dict_Movies()
        match = process.extractOne(movie, mdict.keys())
        ep = mdict[match[0]]
        tv = self.setup_cc(cast)
        tv.play_media(ep, self.plex)
        
        
    def recomend_movie(self):
        pass
        #get top rated movie
        
        #ask, if no
        
        #get recently added movie
        
        #ask, if no then repeat
        
    def get_top_unwatched_movie(self):
        mdict = self.Dict_Movies()
        sort = sorted(mdict.items(), key=lambda x: x[1].rating if isinstance(x[1].rating, float) else 0,  reverse=True)
        list = []
        for m in sort:
            if m[1].viewCount == 0:
                list.append(m[0])
        return list

    def recent_unwatched_movie(self):
        mdict = self.Dict_Movies()
        sort = sorted(mdict.items(), key=lambda x: x[1].addedAt,  reverse=True)
        list = []
        for m in sort:
            if m[1].viewCount == 0:
                list.append(m[0])
        return list


if __name__ == "__main__":
    baseurl = 'http://ServerIP:32400'
    token = 'plextoken'
    plex = SnipsPlex(baseurl, token)
    plex.playTVonDeck(input("show"), 'living  room')
