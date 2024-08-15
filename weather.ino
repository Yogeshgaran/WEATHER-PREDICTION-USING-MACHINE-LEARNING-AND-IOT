#include "DHT.h"

#define DHTPIN 2     // Define the pin connected to the DHT sensor
#define DHTTYPE DHT11   // DHT 11 

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  Serial.begin(9600); 
  dht.begin();
}

void loop() {
  // Wait a few seconds between measurements.
  delay(2000);

  // Reading temperature or humidity takes about 250 milliseconds!
  float humidity = dht.readHumidity();
  // Read temperature as Celsius (the default)
  float temperature = dht.readTemperature();

  // Check if any reads failed and exit early (to try again).
  if (isnan(humidity) || isnan(temperature)) {
    Serial.println("Failed to read from DHT sensor!");
    return;
  }
#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>

const char* ssid = "ARUNAJITH";     // Replace with your WiFi SSID
const char* password = "arunajith"; // Replace with your WiFi password

ESP8266WebServer server(80);

const int trigPin1 = D1;
const int echoPin1 = D2;
const int trigPin2 = D3;
const int echoPin2 = D4;

void setup() {
  Serial.begin(115200);
  pinMode(trigPin1, OUTPUT);
  pinMode(echoPin1, INPUT);
  pinMode(trigPin2, OUTPUT);
  pinMode(echoPin2, INPUT);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  server.on("/", handleRoot);
  server.begin();
  Serial.println("HTTP server started");
}

void loop() {
  server.handleClient();
}

String getCarDiv(String status) {
  String color = (status == "Free") ? "green" : "red";
  return "<div style='width: 100px; height: 50px; background-color: " + color + "; "
         "border-radius: 20px; margin: 20px auto;'></div>";
}

void handleRoot() {
  int distance1 = getDistance(trigPin1, echoPin1);
  int distance2 = getDistance(trigPin2, echoPin2);

  String status1 = (distance1 < 10) ? "Filled" : "Free"; // Threshold distance
  String status2 = (distance2 < 10) ? "Filled" : "Free"; // Threshold distance

  String carDiv1 = getCarDiv(status1);
  String carDiv2 = getCarDiv(status2);

  String html = "<html><head><style>"
                "div.slot { width: 50%; float: left; text-align: center; }"
                "div.car { width: 100px; height: 50px; background-color: red; "
                "border-radius: 20px; margin: 20px auto; }"
                ".free { background-color: green; }"
                ".filled { background-color: red; }"
                "</style></head><body>"
                "<div class='slot'>"
                "<h2>Parking Slot Number 1</h2>"
                "<p>Status: " + status1 + "</p>"
                + carDiv1 +
                "</div>"
                "<div class='slot'>"
                "<h2>Parking Slot Number 2</h2>"
                "<p>Status: " + status2 + "</p>"
                + carDiv2 +
                "</div>"
                "</body></html>";

  server.send(200, "text/html", html);
}

int getDistance(int trigPin, int echoPin) {
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  long duration = pulseIn(echoPin, HIGH);
  int distance = static_cast<int>(duration * 0.034 / 2);
  return distance;
}


  // Print the humidity and temperature
  // Sends the data in a structured format, for example: "54.00,23.00"
  Serial.print(humidity/100);
  Serial.print(",");
  Serial.println(temperature);
}
