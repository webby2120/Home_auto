"""
Controller to interface with the Plex-app.
"""
import time
from pychromecast.controllers import BaseController

STREAM_TYPE_UNKNOWN = "UNKNOWN"
STREAM_TYPE_BUFFERED = "BUFFERED"
STREAM_TYPE_LIVE = "LIVE"

MESSAGE_TYPE = 'type'

TYPE_PLAY = "PLAY"
TYPE_PAUSE = "PAUSE"
TYPE_STOP = "STOP"
TYPE_LOAD = "LOAD"
TYPE_SEEK = "SEEK"

class PlexController(BaseController):
    """ Controller to interact with Plex namespace. """

    def __init__(self):
        super(PlexController, self).__init__(
            "urn:x-cast:plex", "9AC194DC")
        self.app_id="9AC194DC"
        self.namespace="urn:x-cast:plex"
        self.request_id = 0
        self.media_session_id = 0
        self.receiver = None

    def set_volume(self,percent):
        percent = float(percent) / 100
        self._socket_client.receiver_controller.set_volume(percent)

    def volume_up(self,cast):
        cast.volume_up()

    def volume_down(self,cast):
        cast.volume_down()

    def mute(self,cast,status):
        cast.set_volume_muted(status)

    def stop(self):
        """ Send stop command. """
        self.namespace = "urn:x-cast:plex"
        self.request_id += 1
        self.send_message({MESSAGE_TYPE: TYPE_STOP})

    def pause(self):
        """ Send pause command. """
        self.namespace = "urn:x-cast:plex"
        self.request_id += 1
        self.send_message({MESSAGE_TYPE: TYPE_PAUSE})

    def play(self):
        """ Send play command. """
        self.namespace = "urn:x-cast:plex"
        self.request_id += 1
        self.send_message({MESSAGE_TYPE: TYPE_PLAY})


    def play_media(self,item,server):
        #def app_launched_callback():
            #time.sleep(10)
            #self.set_load(item,server)
        receiver_ctrl = self._socket_client.receiver_controller
        #receiver_ctrl.launch_app(self.app_id, callback_function=app_launched_callback)
        receiver_ctrl.launch_app (self.app_id)
        time.sleep(10)
        self.set_load(item,server)

    def set_load(self,item,server):
        transient_token = server.query("/security/token?type=delegation&scope=all").attrib.get('token')
        playqueue = server.createPlayQueue(item)
        playQueueID = playqueue.playQueueID
        self.request_id += 1 # Update
        #Session ID
        address = server._baseurl.split(":")[1][2:]
        port = server._baseurl.split(":")[2]
        self.namespace="urn:x-cast:com.google.cast.media"
        if item.type == "playlist":
            item.key = item.items()[0].key
        true = 'true'
        false = 'false'
        null = 'null'
        msg = {
            "activeTrackIds": None,
            "sessionId": None,
            "requestId": 0,
            "currentTime": 0,
            "media": {
                "textTrackStyle": None,
                "contentId": item.key,
                "customData": {
                    "providerIdentifier": "com.plexapp.plugins.library",
                    "playQueueType": "video",
                    "primaryServer": {
                        "myPlexSubscription": True,
                        "protocol": "http",
                        "transcoderVideo": True,
                        "address": address,
                        "transcoderVideoRemuxOnly": False,
                        "port": port,
                        "transcoderAudio": True,
                        "accessToken": transient_token,
                        "isVerifiedHostname": False,
                        "version": server.version,
                        "machineIdentifier": server.machineIdentifier
                    },
                    #"containerKey": "/playQueues/2236?own=1",
                    "containerKey": "/playQueues/{}?own=1&window=200".format(playQueueID),
                    "offset": 0,
                    "audioBoost": 100,
                    "user": {"username": server.myPlexUsername},
                    "directPlay": True,
                    "server": {
                        "myPlexSubscription": True,
                        "protocol": "http",
                        "transcoderVideo": True,
                        "address": address,
                        "transcoderVideoRemuxOnly": False,
                        "port": port,
                        "transcoderAudio": True,
                        "accessToken": transient_token,
                        "isVerifiedHostname": False,
                        "version": server.version,
                        "machineIdentifier": server.machineIdentifier
                    },
                    "directStream": True
                },
                "tracks": None,
                "streamType": "BUFFERED",
                "duration": None,
                "metadata": None
            },
            "customData": None,
            "type": "LOAD",
            "autoplay": True
        }
        self.send_message(msg, inc_session_id=True)


    def receive_message(self,message,data):
        """ Called when a media message is received. """
        if data[MESSAGE_TYPE] == TYPE_MEDIA_STATUS:
            return True

        else:
            return False
