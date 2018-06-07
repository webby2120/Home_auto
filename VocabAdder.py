import paho.mqtt.publish as publish
import json


class update_vocab:

    def __init__(self, name, values, mqtt_host):
        self.name = name
        self.values = values
        self.mqtt_host = mqtt_host
    def update(self):
        jsonstring = {"operations": [("add", {self.name : self.values})]}
        jsonstring = json.dumps(jsonstring)
        publish.single("hermes/asr/inject", jsonstring, hostname=self.mqtt_host)
        print(jsonstring)



if __name__ == '__main__':
    #this example will add 3 new sonfs to the snips vocab for song_name
    songs = ['song 1', 'song 2', 'ect...']
    update_vocab("song_name", songs, "192.168.0.93").update()