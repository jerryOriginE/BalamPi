#include <WiFi.h>
#include <WebServer.h>
#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <HTTPClient.h>

const int buttonPin = 4;
bool lastButtonState = HIGH;

const char* piIP = "192.168.1.50"; // gotta change

const char* ssid = "";
const char* password = "";

WebServer server(80);
LiquidCrystal_I2C lcd(0x27, 16, 2);

String currentMessage = "";
bool scrollMessage = false;
unsigned long lastScroll = 0;
int scrollPos = 0;

void handleDisplay() {
  if (!server.hasArg("text")) {
    server.send(400, "text/plain", "Missing text parameter");
    return;
  }

  currentMessage = server.arg("text");

  if (currentMessage.length() <= 32) {
    scrollMessage = false;

    lcd.clear();
    lcd.setCursor(0, 0);
    lcd.print(currentMessage.substring(0, 16));

    if (currentMessage.length() > 16) {
      lcd.setCursor(0, 1);
      lcd.print(currentMessage.substring(16, 32));
    }
  } else {
    scrollMessage = true;
    scrollPos = 0;
  }

  server.send(200, "text/plain", "Message displayed");
}

void updateScrollingText() {
  if (!scrollMessage)
    return;

  if (millis() - lastScroll < 600)
    return;

  lastScroll = millis();

  String padded = currentMessage + "                "; // 16 spaces

  String window = padded.substring(
      scrollPos,
      min(scrollPos + 32, (int)padded.length()));

  while (window.length() < 32)
    window += " ";

  lcd.clear();

  lcd.setCursor(0, 0);
  lcd.print(window.substring(0, 16));

  lcd.setCursor(0, 1);
  lcd.print(window.substring(16, 32));

  scrollPos++;

  if (scrollPos >= padded.length())
    scrollPos = 0;
}

void sendButtonPress() {

  if (WiFi.status() != WL_CONNECTED)
    return;

  HTTPClient http;

  String url = "http://" + String(piIP) + ":5000/button";

  http.begin(url);

  int responseCode = http.POST("");

  Serial.println("Response: ");
  Serial.println(responseCode);

  http.end();
}

void setup() {
  Serial.begin(9600);
  delay(1000);

  pinMode(buttonPin, INPUT_PULLUP);
  Wire.begin(21, 22);

  lcd.init();
  lcd.backlight();
  lcd.print("Connecting...");

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
  }

  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Ready!");

  Serial.println(WiFi.localIP());

  
  lcd.setCursor(0, 1);
  lcd.print(WiFi.localIP());

  server.on("/display", handleDisplay);
  server.begin();
}

void loop() {
  server.handleClient();

  updateScrollingText();

  bool currentState = digitalRead(buttonPin);

  if (currentState == LOW && lastButtonState == HIGH) {
    Serial.println("Button pressed");

    sendButtonPress();

    delay(50); // debounce
  }

  lastButtonState = currentState;
}