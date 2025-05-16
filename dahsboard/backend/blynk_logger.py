import requests
import sqlite3
import time
from datetime import datetime

DB_FILE = "blynk_data.db"
BLYNK_TOKEN = "FpQ6nvN9nATbU1E6qNbcfqU5XMmlYQI3"
BLYNK_API = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}&v1&v2&v3&v6"

def save_to_db(soil, temp, hum, light):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_data (soil_moisture, temperature, humidity, light)
        VALUES (?, ?, ?, ?)
    ''', (soil, temp, hum, light))
    conn.commit()
    conn.close()

def collect_loop():
    while True:
        try:
            res = requests.get(BLYNK_API)
            data = res.json()
            print("📥 Received:", data)
            save_to_db(data["v1"], data["v2"], data["v3"], data["v6"])
        except Exception as e:
            print("❌ Error:", e)
        time.sleep(10)

if __name__ == "__main__":
    collect_loop()