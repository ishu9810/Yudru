#include <WiFi.h>
#include <esp_now.h>
#include "config.h"

void onDataRecv(const uint8_t* mac, const uint8_t* incomingData, int len) {
  Serial.write(incomingData, len); // Bridge mesh command to Betaflight UART
}

void setup() {
  Serial.begin(UART_BAUDRATE);
  WiFi.mode(WIFI_STA);
  esp_wifi_set_channel(WIFI_CHANNEL, WIFI_SECOND_CHAN_NONE);

  if (esp_now_init() != ESP_OK) {
    Serial.println("ESP-NOW init failed");
    return;
  }

  esp_now_register_recv_cb(onDataRecv);
  Serial.println("ESP-NOW mesh bridge started");
}

void loop() {
  if (Serial.available()) {
    uint8_t buffer[250];
    int len = Serial.readBytes(buffer, sizeof(buffer));
    esp_now_send(nullptr, buffer, len); // Broadcast to all peers
  }
  delay(5);
}
