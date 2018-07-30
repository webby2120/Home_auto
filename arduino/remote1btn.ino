#include <ESP8266WiFi.h>
#include <Wire.h>
#include <PubSubClient.h>



#define wifi_ssid "Webbys_Wondrous_WIFI"
#define wifi_password "FUCK_OFF_PEASANT"
#define mqtt_server "192.168.0.93"
#define Button_topic "Remote/Button"


WiFiClient espClient;
PubSubClient client(espClient);

long lastMsg = 0;
int btn1 = D3;       
int btn1state = 0;



void setup() {
  Serial.begin(115200);
  delay(10);
  pinMode(btn1, INPUT_PULLUP);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
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
    if (client.connect("Remote_2")) {
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

void loop() {

  if (!client.connected()) 
  {
    reconnect();
  }
  client.loop();  
  btn1state = digitalRead(btn1);  
  if (btn1state == LOW)
  {
    Serial.println("button 1 pressed");
    client.publish(Button_topic, "1", true);
    delay(500);
  } 
  

}

//}
