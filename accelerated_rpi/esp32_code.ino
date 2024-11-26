// a copy of what is programmed onto the esp32 microcontroller

#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "CMU-DEVICE";
// const char* password = "handsytunes"; // Uncomment if your Wi-Fi requires a password

int redPin = 25;
int greenPin = 26;
int bluePin = 27;

WebServer server(80);

void setup() {
  Serial.begin(115200);
  
  // Connect to Wi-Fi
  WiFi.begin(ssid);
  // Uncomment the next line if a password is required
  // WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  Serial.println("Connected to WiFi!");

  // Define endpoints and corresponding LED control
  server.on("/red", HTTP_GET, []() {
    Serial.println("Red LED request received");
    // Set the LED to red
    digitalWrite(redPin, LOW);    // Red on
    digitalWrite(greenPin, HIGH); // Green off
    digitalWrite(bluePin, HIGH);  // Blue off
    server.send(200, "text/plain", "LED set to red");
  });

  server.on("/green", HTTP_GET, []() {
    Serial.println("Green LED request received");
    // Set the LED to green
    digitalWrite(redPin, HIGH);   // Red off
    digitalWrite(greenPin, LOW);  // Green on
    digitalWrite(bluePin, HIGH);  // Blue off
    server.send(200, "text/plain", "LED set to green");
  });

  server.on("/blue", HTTP_GET, []() {
    Serial.println("Blue LED request received");
    // Set the LED to blue
    digitalWrite(redPin, HIGH);   // Red off
    digitalWrite(greenPin, HIGH); // Green off
    digitalWrite(bluePin, LOW);   // Blue on
    server.send(200, "text/plain", "LED set to blue");
  });

  server.on("/off", HTTP_GET, []() {
    Serial.println("Off LED request received");
    // Set the LED to off
    digitalWrite(redPin, HIGH);   // Red off
    digitalWrite(greenPin, HIGH); // Green off
    digitalWrite(bluePin, HIGH);   // Blue on
    server.send(200, "text/plain", "LED set to off");
  });

  // Start the server
  server.begin();

  // Initialize LED pins as output
  pinMode(redPin, OUTPUT);
  pinMode(greenPin, OUTPUT);
  pinMode(bluePin, OUTPUT);
}

void loop() {
  // Handle client requests
  server.handleClient();
}
