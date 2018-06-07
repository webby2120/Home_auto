import paho.mqtt.publish as publish
import webcolors



class WebbyLights:

    def __init__(self, room):
        self.room = room
        self.state = [0, 0, 0, 255]

    def set_lights(self, r, g, b, w):
        publish.single("lights/{}/color/blue".format(self.room), str(b), hostname="192.168.0.93")
        publish.single("lights/{}/color/red".format(self.room), str(r), hostname="192.168.0.93")
        publish.single("lights/{}/color/green".format(self.room), str(g), hostname="192.168.0.93")
        publish.single("lights/{}/color/white".format(self.room), str(w), hostname="192.168.0.93")
        self.state = [r, g, b, w]

    def on(self):
        self.set_lights(0, 0, 0, 255)

    def off(self):
        self.set_lights(0, 0, 0, 0)

    def toggle(self):
        if self.state == [0, 0, 0, 0]:
            self.on()
        else:
            self.off()

    def set_color(self, color):
        try:
            x = webcolors.name_to_rgb(color.replace(" ", ""))
            self.set_lights(x[0], x[1], x[2], 0)
            print(x[0], x[1], x[2])
        except:
            pass

    def dim(self):
        i = 0
        for b in self.state:
            if b > 50:
                b = b - 50
            self.state[i] = b
            i = i + 1
        self.set_lights(self.state[0],self.state[1],self.state[2],self.state[3])

    def brighten(self):
        i = 0
        for b in self.state:
            if b < 200:
                if b > 1:
                    b = b + 50
            self.state[i] = b
            i = i + 1
        self.set_lights(self.state[0], self.state[1], self.state[2], self.state[3])