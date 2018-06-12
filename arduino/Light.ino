//http://www.esp8266learning.com/wemos-webserver-example.php

#include <ESP8266WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>
#include <my92xx.h>
#define MY92XX_MODEL    MY92XX_MODEL_MY9291     // The MY9291 is a 4-channel driver, usually for RGBW lights
#define MY92XX_CHIPS    1                       // No daisy-chain
#define MY92XX_DI_PIN   13                      // DI GPIO
#define MY92XX_DCKI_PIN 15                      // DCKI GPIO



#define wifi_ssid "WIFI SSID"
#define wifi_password "WIFI Password"
#define mqtt_server "MQTT Server"
//Assign color to gpio
String inString = "";


WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;


my92xx _my92xx = my92xx(MY92XX_MODEL, MY92XX_CHIPS, MY92XX_DI_PIN, MY92XX_DCKI_PIN, MY92XX_COMMAND_DEFAULT);


void setup() {

  Serial.begin(115200);
  delay(10);
  _my92xx.setChannel(3, 255); // assume channel 0 is RED
  _my92xx.setState(true);
  _my92xx.update();
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  
}

void setup_wifi() {
  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(wifi_ssid);

  WiFi.begin(wifi_ssid, wifi_password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
	
    if (client.connect("Bulb1")) { //make sure to change Bulb1 to a unique name
      client.subscribe("lights/bedroom/#"); //change rooms to suite
      Serial.println("connected");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void callback(char* topic, byte* payload, unsigned int length) {
  for (int i=0;i<length;i++) {
    inString += (char)payload[i];
  }
  int msg = inString.toInt();
  if (String(topic) == "lights/bedroom/power/on") {
    light_on();
  }
  if (String(topic) == "lights/bedroom/power/off") {
    light_off();
  }
  if (String(topic) == "lights/bedroom/color/red") {
    _my92xx.setChannel(0, msg);
  }
  if (String(topic) == "lights/bedroom/color/green") {
    _my92xx.setChannel(1, msg);
  }
  if (String(topic) == "lights/bedroom/color/blue") {
    _my92xx.setChannel(2, msg);
  }
  if (String(topic) == "lights/bedroom/color/white") {
    _my92xx.setChannel(3, msg);
  }
  _my92xx.update();
  inString = "";
}




void light_on(){
  Serial.print("turn light on ");
  Serial.println();
  _my92xx.setChannel(3, 255);

}

void light_off(){
  Serial.print("turn light off ");
  Serial.println();
  _my92xx.setChannel(0, 0);
  _my92xx.setChannel(1, 0);
  _my92xx.setChannel(2, 0);
  _my92xx.setChannel(3, 0);
}


void loop() {

    if (!client.connected()) {
    reconnect();
    }
  client.loop();



}

