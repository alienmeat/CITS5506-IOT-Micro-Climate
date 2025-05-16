#include "fan_control.h"
#include "lamp_control.h"

void setup() {
  Serial.begin(115200);
  Serial.println("Fan & Lamp Test Starting...");

  initFan();
  initLamp();
}

void loop() {
  Serial.println("Fan ON");
  fanOn();
  delay(2000);

  Serial.println("Lamp ON");
  lampOn();
  delay(2000);

  Serial.println("Fan OFF");
  fanOff();
  delay(2000);

  Serial.println("Lamp OFF");
  lampOff();
  delay(2000);
}



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





