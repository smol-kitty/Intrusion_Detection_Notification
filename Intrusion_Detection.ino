#define PIR_SENSOR_PIN D1      
#define BUZZER_PIN D2          

#include <ESP8266WiFi.h>

const char* ssid = "<Wifi SSID>";
const char* password = "<Wifi Password>";
const char* serverIP = "<Server IP>";
const int serverPort = <SERVER PORT>;

void setup() {
  Serial.begin(115200);
  pinMode(PIR_SENSOR_PIN, INPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi");
}

void loop() {
  int pirState = digitalRead(PIR_SENSOR_PIN);

  if (pirState == HIGH) {
    Serial.println("Motion detected!");

    digitalWrite(BUZZER_PIN, HIGH);

    sendTriggerRequest();

    while (digitalRead(PIR_SENSOR_PIN) == HIGH) {
      delay(100); 
    }

  digitalWrite(BUZZER_PIN, LOW);

  } else {
    Serial.println("No motion detected.");
  }

  delay(1000);
}

void sendTriggerRequest() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClient client;
    if (client.connect(serverIP, serverPort)) {
      client.println("GET /trigger_camera HTTP/1.1");
      client.println("Host: " + String(serverIP));
      client.println("Connection: close");
      client.println();

      while (client.connected() && !client.available()) {
        delay(10);
      }
      while (client.available()) {
        String line = client.readStringUntil('\n');
        Serial.println(line);
      }
      client.stop();
      Serial.println("Image capture request sent");
    } else {
      Serial.println("Connection to server failed");
    }
  } else {
    Serial.println("WiFi not connected");
  }
}
