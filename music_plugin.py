import pychromecast
from gmusicapi import Mobileclient
import random
import time
from fuzzywuzzy import process
import billboard


class Music_Player:
    def __init__(self, cast, username, password, devId):
        self.cast = cast.lower()
        self.mc = self.Get_MC(self.cast)
        self.username = username
        self.password = password
        self.devId = devId
        self.logged_in = False
        self.api = self.Google_Auth()
        self.playing = False
        self.stop = False
        self.songinfo = {}

    def Get_MC(self, name):
        chromecasts = pychromecast.get_chromecasts()
        for cc in chromecasts:
            print(cc.device.friendly_name)
            if cc.device.friendly_name.lower() == name:
                print("device found")
                self.cc = cc
                mc = cc.media_controller
                return mc

    def Google_Auth(self):
        api = Mobileclient()
        attempts = 0
        while not self.logged_in and attempts < 3:
            self.logged_in = api.login(self.username, self.password, self.devId)
            attempts += 1
        if api.is_authenticated():
            self.logged_in = True
        return api

    def Get_SongID(self, song):
        if not self.api.is_authenticated():
            self.Google_Auth()
        song = song.replace(' ','_')
        results = self.api.search(song, 3)
        song_id = results['song_hits'][0]['track']['storeId']
        return song_id

    def Get_SongURL(self, songId):
        if not self.api.is_authenticated():
            self.Google_Auth()
        URL = self.api.get_stream_url(songId)
        return URL

    def Play_SongID(self, songId):
        """play song by ID"""
        try:
            self.songinfo = self.api.get_track_info(songId)
        except:
            self.songinfo = {"invalid": "invalid"}
        if not self.mc._socket_client:
            self.mc = self.Get_MC(self.cast)
        self.mc.play_media(self.Get_SongURL(songId), 'audio/mp3')
        self.mc.block_until_active()

    def Play_Song(self, song):
        """play song by song name"""
        ID = self.Get_SongID(song)
        self.Play_SongID(ID)

    def Shuffle_All(self):
        while not self.stop:
            if not self.api.is_authenticated():
                self.Google_Auth()
            library = self.api.get_all_songs()
            rand = random.randint(0, len(library))
            self.Play_SongID(library[rand]['storeId'])
            self.Wait_For_Song()
            print("finished playing next song")
        print("music stopped  ")

    def Wait_For_Song(self):
        time.sleep(20)
        i = 0
        while not self.mc.status.player_is_idle and not self.stop:
            time.sleep(1)
            i += 1
            if i > 60:
                i = 0
                print(self.mc.status)

    def Stop(self):
        self.stop = True
        self.mc.stop()
        self.songinfo = {}
        self.cc.quit_app()


    def Skip(self):
        self.mc.stop()

    def Play_Playlist(self, playlist):
        playlist = self.Get_Playlist(playlist)
        while not self.stop:
            if not self.api.is_authenticated():
                self.Google_Auth()

            rand = random.randint(0, len(playlist))

            try:
                self.Play_SongID(playlist[rand]['track']['storeId'])
                self.Wait_For_Song()
                print("finished playing next song")
            except:
                print("Song {} is missing from playlist".format(rand))
        print("music stopped  ")

    def Get_Playlist(self, name):
        playlists = self.api.get_all_user_playlist_contents()
        for playlist in playlists:
            if name.lower() == playlist['name'].lower():
                List = playlist['tracks']
                return List

    def List_Playlists(self):
        lists = self.api.get_all_playlists()
        playlists = list()
        for l in lists:
            playlists.append(l['name'])
        return playlists

    def List_Songs(self):
        s_list = self.api.get_all_songs()
        chart = billboard.ChartData('hot-100')
        songs = list()
        for song in s_list:
            songs.append(song['title'])
        for song in chart.entries:
            print(song.title)
        return songs

    def fuzz_playlist(self, pl, acuracy):
        # try and soft match requested playlist to one of you playlists
        choices = self.List_Playlists()
        match = process.extractOne(pl, choices)
        print(match)
        if match[1] >= acuracy:
            return match[0]

    def fuzz_song(self, song, acuracy):
        # try and soft match song to a song from your song lists
        choices = self.List_Songs()
        match = process.extractOne(song, choices)
        print(match)
        if match[1] >= acuracy:
            return match[0]



# basic usage demo
if __name__ == '__main__':
    chromecast = input("what chromecast would you like to use?")
    gmail = input("what is your gmail address?")
    password = input("what is your gmail password?")
    devid = input("what is your device ID?")
    player = Music_Player(chromecast, gmail, password, devid)

    print("player set up")
    choice = ""
    while choice != 'x':
        choice = input("what would you like to do? \n press 1 to play song \n press 2 to play a playlist \n press 3 to stop the music \n press x to exit")
        if choice == '1':
            player.Play_Song(input('what song would you like to play?'))
        elif choice == '2':
            print("what playlist would you like to play?")
            list = player.List_Playlists()
            i = 0
            for plist in list:
                print("{}: {}".format(i,plist))
                i = i + 1
            # this will tie up the thread, best to run the whole player in its own thread when using in production
            player.Play_Playlist(list[int(input("playlist number:"))])
        elif choice == '3':
            player.Stop()