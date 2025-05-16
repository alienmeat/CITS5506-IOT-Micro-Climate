#define BLYNK_TEMPLATE_ID "TMPL6H5aW08du"
#define BLYNK_TEMPLATE_NAME "smart garden"
#define BLYNK_AUTH_TOKEN "FpQ6nvN9nATbU1E6qNbcfqU5XMmlYQI3"

#include <Wire.h>
#include <WiFi.h>
#include <BlynkSimpleEsp32.h>

#include "sensor_bme280.h"
#include "sensor_light.h"
#include "sensor_soil.h"
#include "fan_control.h"
#include "lamp_control.h"
#include "pump_control.h"

// WiFi credentials
char ssid[] = "iH";
char pass[] = "nihaonihao";

void setup() {
  Serial.begin(9600);

  // Start I2C on custom SDA/SCL pins
  Wire.begin(BME_SDA, BME_SCL);

  // Initialize sensors
  if (!initBME280()) {
    Serial.println("❌ BME280 initialization failed!");
    while (1);
  }

  if (!initLightSensor()) {
    Serial.println("❌ VEML6030 initialization failed!");
    while (1);
  }

  initSoilSensor();

  // Initialize actuators
  initFan();
  initLamp();
  initPump();

  // Connect to WiFi
  WiFi.begin(ssid, pass);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\n✅ WiFi connected");

  // Connect to Blynk
  Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
}

void loop() {
  Blynk.run();

  // Read sensors
  float temp = readTemperatureC();
  float hum = readHumidity();
  float pres = readPressure();
  float lux = readLightLux();
  int soil = readSoilPercent();

  // Serial output
  Serial.println("📊 Sensor Readings:");
  Serial.printf("🌡 Temp: %.2f °C\n", temp);
  Serial.printf("💧 Hum: %.2f %%\n", hum);
  Serial.printf("🌬 Pres: %.2f hPa\n", pres);
  Serial.printf("🔆 Lux: %.2f\n", lux);
  Serial.printf("🌱 Soil Moisture: %d %%\n", soil);
  Serial.println("-----------------------------\n");

  // Send to Blynk
  Blynk.virtualWrite(V2, temp);
  Blynk.virtualWrite(V3, hum);
  Blynk.virtualWrite(V10, pres);
  Blynk.virtualWrite(V6, lux);
  Blynk.virtualWrite(V1, soil);

  delay(2000);
}

// Fan control from Blynk
BLYNK_WRITE(V7) {
  int state = param.asInt();
  if (state) fanOn();
  else fanOff();
  Serial.println(state ? "🌀 Fan ON" : "🌀 Fan OFF");
}

// Lamp control from Blynk
BLYNK_WRITE(V11) {
  int state = param.asInt();
  if (state) lampOn();
  else lampOff();
  Serial.println(state ? "💡 Lamp ON" : "💡 Lamp OFF");
}

// Pump control from Blynk
BLYNK_WRITE(V4) {
  int state = param.asInt();
  if (state) pumpOn();
  else pumpOff();
  Serial.println(state ? "💧 Pump ON" : "💧 Pump OFF");
}



// #define BLYNK_TEMPLATE_ID "TMPL6H5aW08du"
// #define BLYNK_TEMPLATE_NAME "smart garden"
// #define BLYNK_AUTH_TOKEN "FpQ6nvN9nATbU1E6qNbcfqU5XMmlYQI3"

// #include <Wire.h>
// #include <WiFi.h>
// #include <BlynkSimpleEsp32.h>

// #include "sensor_bme280.h"
// #include "sensor_light.h"
// #include "sensor_soil.h"  // 🌱 Soil sensor header

// // WiFi credentials
// char ssid[] = "iH";      // Replace with your WiFi SSID
// char pass[] = "nihaonihao";  // Replace with your WiFi password

// void setup() {
//   Serial.begin(9600);

//   // Start I2C on custom SDA/SCL pins
//   Wire.begin(BME_SDA, BME_SCL);

//   // Initialize sensors
//   if (!initBME280()) {
//     Serial.println("❌ BME280 initialization failed!");
//     while (1);
//   }

//   if (!initLightSensor()) {
//     Serial.println("❌ VEML6030 initialization failed!");
//     while (1);
//   }

//   initSoilSensor();  // 🌱 Soil sensor

//   // Connect to WiFi
//   WiFi.begin(ssid, pass);
//   Serial.print("Connecting to WiFi");
//   while (WiFi.status() != WL_CONNECTED) {
//     delay(500);
//     Serial.print(".");
//   }
//   Serial.println("\n✅ WiFi connected");

//   // Connect to Blynk
//   Blynk.begin(BLYNK_AUTH_TOKEN, ssid, pass);
// }

// void loop() {
//   Blynk.run();

//   // Read sensors
//   float temp = readTemperatureC();
//   float hum = readHumidity();
//   float pres = readPressure();
//   float lux = readLightLux();
//   int soil = readSoilPercent();  // 🌱 Moisture %

//   // Print to Serial Monitor
//   Serial.println("📊 Sensor Readings:");
//   Serial.printf("🌡 Temp: %.2f °C\n", temp);
//   Serial.printf("💧 Hum: %.2f %%\n", hum);
//   Serial.printf("🌬 Pres: %.2f hPa\n", pres);
//   Serial.printf("🔆 Lux: %.2f\n", lux);
//   Serial.printf("🌱 Soil Moisture: %d %%\n", soil);
//   Serial.println("-----------------------------\n");

//   // Send data to Blynk
//   Blynk.virtualWrite(V2, temp);
//   Blynk.virtualWrite(V3, hum);
//   Blynk.virtualWrite(V10, pres);  // Optional
//   Blynk.virtualWrite(V6, lux);
//   Blynk.virtualWrite(V1, soil);  // 🌱 Soil %

//   delay(2000);
// }




// #include "fan_control.h"
// #include "lamp_control.h"

// void setup() {
//   Serial.begin(115200);
//   Serial.println("Fan & Lamp Test Starting...");

//   initFan();
//   initLamp();
// }

// void loop() {
//   Serial.println("Fan ON");
//   fanOn();
//   delay(2000);

//   Serial.println("Lamp ON");
//   lampOn();
//   delay(2000);

//   Serial.println("Fan OFF");
//   fanOff();
//   delay(2000);

//   Serial.println("Lamp OFF");
//   lampOff();
//   delay(2000);
// }



// #include <Wire.h>
// #include "sensor_bme280.h"
// #include "sensor_light.h"

// void setup() {
//   Serial.begin(9600);
//   delay(1000);

//   if (initBME280()) {
//     Serial.println("✅ BME280 initialized.");
//   } else {
//     Serial.println("❌ Failed to initialize BME280.");
//     while (1);
//   }

//   if (initLightSensor()) {
//     Serial.println("✅ VEML6030 initialized.");
//   } else {
//     Serial.println("❌ Failed to initialize VEML6030.");
//     while (1);
//   }
// }

// void loop() {
//   Serial.println("📊 Sensor Readings:");

//   // BME280
//   Serial.print("🌡 Temperature: ");
//   Serial.print(readTemperatureC());
//   Serial.println(" °C");

//   Serial.print("💧 Humidity: ");
//   Serial.print(readHumidity());
//   Serial.println(" %");

//   Serial.print("🌬 Pressure: ");
//   Serial.print(readPressure());
//   Serial.println(" hPa");

//   // VEML6030
//   Serial.print("🔆 Ambient Light: ");
//   Serial.print(readLightLux());
//   Serial.println(" Lux");

//   Serial.println("-----------------------------\n");
//   delay(2000);
// }






// #include <Wire.h>

// void setup() {
//   Serial.begin(115200);
//   Serial.println("🔌 I2C Scanner Started");

//   Wire.begin(5, 6);  // Your custom SDA, SCL pins

//   delay(500);
//   Serial.println("🔍 Scanning for I2C devices...");

//   int found = 0;
//   for (byte address = 1; address < 127; address++) {
//     Wire.beginTransmission(address);
//     byte error = Wire.endTransmission();

//     if (error == 0) {
//       Serial.print("✅ Found device at 0x");
//       if (address < 16) Serial.print("0");
//       Serial.println(address, HEX);
//       found++;
//     }
//   }

//   if (found == 0) {
//     Serial.println("❌ No I2C devices found.");
//   } else {
//     Serial.print("🔎 Total found: ");
//     Serial.println(found);
//   }
// }

// void loop() {
//   // do nothing
// }

//----------------------------

// #include "wifi_http_client.h"
// #include "sensor_bme280.h"
// #include "sensor_soil.h"

// void setup() {
//   Serial.begin(115200);
//   connectToWiFi();

//   // Initialize sensors
//   if (!initBME280()) {
//     Serial.println("❌ BME280 init failed.");
//     while (1); // Stop if sensor not found
//   }

//   initSoilSensor();
// }

// void loop() {
//   // Get live sensor data
//   float temp = readTemperatureC();
//   float hum = readHumidity();
//   float press = readPressure();
//   int soil = readSoilPercent();

//   // Send data
//   sendSensorData(temp, hum, press, soil);
//   delay(5000);  // every 5 seconds
// }





