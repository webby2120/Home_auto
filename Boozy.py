import paho.mqtt.publish as publish
import time
from fuzzywuzzy import process


class Boozy:

    def __init__(self, mqtt):
        #what dink is on what pump and how long to run the pump for
        self.menu = {"Gin": (0, 15), "Tonic": (1, 30), "Port": (2, 40)}
        self.mqttserver = mqtt

    def make(self, input):
        #uses the menue to get the run time for each pump
        p = [0, 0, 0]
        for drink in input:
            match = process.extractOne(drink, self.menu.keys())
            p[self.menu[match[0]][0]] = self.menu[match[0]][1]
        self.run_pumps(p)

    def run_pumps(self, p):
        publish.single("boozy/pump/1", p[0], hostname=self.mqttserver)
        time.sleep(p[0] + 1)
        publish.single("boozy/pump/2", p[1], hostname= self.mqttserver)
        time.sleep(p[1] + 1)
        publish.single("boozy/pump/3", p[2], hostname= self.mqttserver)
        time.sleep(p[2] + 1)


if __name__ == '__main__':
    boozy = Boozy('192.168.0.93')
    order = ['port']
    boozy.make(order)