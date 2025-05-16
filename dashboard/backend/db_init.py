import sqlite3

conn = sqlite3.connect("blynk_data.db")
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    soil_moisture INTEGER,
    temperature REAL,
    humidity REAL,
    light INTEGER
)
''')

conn.commit()
conn.close()
print("initiation done")