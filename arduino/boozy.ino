//http://www.esp8266learning.com/wemos-webserver-example.php

#include <ESP8266WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>


#define wifi_ssid "SSID"
#define wifi_password "Password"
#define mqtt_server "Server IP"
//Assign color to gpio
#define Pump1 D5
#define Pump2 D6
#define Pump3 D7
String inString = "";


WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;



void setup() {
  pinMode(Pump1, OUTPUT);
  pinMode(Pump2, OUTPUT);
  pinMode(Pump3, OUTPUT);
  Serial.begin(115200);
  delay(10);

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
    if (client.connect("Boozy")) {
      client.subscribe("boozy/pump/#");
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
  Serial.println("msg recived");
  for (int i=0;i<length;i++) {
    inString += (char)payload[i];
  }
  int msg = inString.toInt();
  Serial.println(msg);
  if (String(topic) == "boozy/pump/1") {
    Serial.println("pump 1 startt");
    set_pump(1, msg);
  }
  if (String(topic) == "boozy/pump/2") {
    Serial.println("pump 2 startt");
    set_pump(2, msg);
  }
  if (String(topic) == "boozy/pump/3") {
    Serial.println("pump 3 startt");
    set_pump(3, msg);
  }
  inString = "";
  Serial.println("end callback");
}


void set_pump(int pump, int amount){
  Serial.print("running pump [");
  Serial.print(pump);
  Serial.print("] ");
  Serial.print("For [");
  Serial.print(amount);
  Serial.print("]Seconds ");
  Serial.println();
  int i = 0;
  if (pump == 1){
    digitalWrite(Pump1, HIGH);   // turn the LED on (HIGH is the voltage level)
    while(i < amount){
    delay(1000);  
    i++;  
    client.loop();
    }
    digitalWrite(Pump1, LOW);
  }
    if (pump == 2){
    digitalWrite(Pump2, HIGH);   // turn the LED on (HIGH is the voltage level)
    while(i < amount){
      delay(1000);  
      i++;  
      client.loop();
    }                     // wait for a second
    digitalWrite(Pump2, LOW);
  }
    if (pump == 3){
    digitalWrite(Pump3, HIGH);   // turn the LED on (HIGH is the voltage level)
    while(i < amount){
      delay(1000);  
      i++;  
      client.loop();
    }                     // wait for a second
    digitalWrite(Pump3, LOW);
  }
  Serial.print(pump);
  Serial.println("finished pumping");
  
}

void loop() {

    if (!client.connected()) {
    reconnect();
    }
  client.loop();
  //Serial.println("looping");
  Serial.println(client.state());
  
  }



