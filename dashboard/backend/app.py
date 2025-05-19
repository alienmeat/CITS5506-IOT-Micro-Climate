from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import threading
import requests
import time
import os
from datetime import datetime

# ========================= 
# db init
# =========================
DB_FILE = "blynk_data.db"
BLYNK_TOKEN = "FpQ6nvN9nATbU1E6qNbcfqU5XMmlYQI3"
BLYNK_API = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}&v1&v2&v3&v6&v10"
BLYNK_WRITE_API = f"https://blynk.cloud/external/api/update?token={BLYNK_TOKEN}"

DEFAULT_SETTINGS = {
    "V8": 0,        # Smart Control default off
    "V20": 40,      # Pump ON Threshold
    "V21": 10,      # Fan Interval
    "V22": 300,     # Lamp ON Threshold
    "V23": 60,      # Pump OFF Threshold
    "V24": 500,     # Lamp OFF Threshold
    "V25": 5        # Fan Duration
}

def get_safe_connection():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

def check_table_exists(conn, table_name):
    """Check if the specified table exists"""
    cursor = conn.cursor()
    cursor.execute(f"""
        SELECT name 
        FROM sqlite_master 
        WHERE type='table' AND name='{table_name}';
    """)
    return cursor.fetchone() is not None

def init_db():
    # db init
    db_exists = os.path.exists(DB_FILE)
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Create sensor_data table if it doesn't exist
    if not check_table_exists(conn, "sensor_data"):
        print("📊 Creating sensor_data table...")
        cursor.execute('''
            CREATE TABLE sensor_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                soil_moisture REAL,
                temperature REAL,
                humidity REAL,
                light REAL,
                pressure REAL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ sensor_data table created")
    else:
        print("✅ sensor_data table already exists")
        
        # Check if we need to rename the Pressure column to pressure
        try:
            cursor.execute("SELECT Pressure FROM sensor_data LIMIT 1")
            # If there's no error, column exists with capital P
            print("⚠️ Renaming 'Pressure' column to 'pressure'...")
            cursor.execute("ALTER TABLE sensor_data RENAME COLUMN Pressure TO pressure")
            print("✅ Column renamed successfully")
        except sqlite3.OperationalError:
            # Column might not exist or is already lowercase
            pass
    
    # Create control_history table if it doesn't exist
    if not check_table_exists(conn, "control_history"):
        print("📊 Creating control_history table...")
        cursor.execute('''
            CREATE TABLE control_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pin TEXT NOT NULL,
                value REAL NOT NULL,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        print("✅ control_history table created")
    else:
        print("✅ control_history table already exists")
    
    # Create current_settings table if it doesn't exist
    if not check_table_exists(conn, "current_settings"):
        print("📊 Creating current_settings table...")
        cursor.execute('''
            CREATE TABLE current_settings (
                pin TEXT PRIMARY KEY,
                value REAL NOT NULL,
                description TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default settings
        for pin, value in DEFAULT_SETTINGS.items():
            pin_descriptions = {
                "V8": "Smart Control",
                "V20": "Pump ON Threshold",
                "V21": "Fan Interval",
                "V22": "Lamp ON Threshold",
                "V23": "Pump OFF Threshold",
                "V24": "Lamp OFF Threshold",
                "V25": "Fan Duration"
            }
            description = pin_descriptions.get(pin, f"Unknown Pin {pin}")
            
            cursor.execute('''
                INSERT INTO current_settings (pin, value, description)
                VALUES (?, ?, ?)
            ''', (pin, value, description))
        
        print("✅ current_settings table created with default values")
    else:
        print("✅ current_settings table already exists")
    
    # Check if device operation history table exists
    if not check_table_exists(conn, "device_operation_history"):
        cursor.execute('''
            CREATE TABLE device_operation_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device TEXT NOT NULL,
                status INTEGER NOT NULL,  -- 1 for on, 0 for off
                start_time DATETIME NOT NULL,
                end_time DATETIME,        -- NULL means device is still running
                duration INTEGER,         -- Runtime in seconds
                reason TEXT               -- Why the operation occurred (e.g., smart control, manual)
            )
        ''')
    
    # Check if device current status table exists
    if not check_table_exists(conn, "device_current_status"):
        cursor.execute('''
            CREATE TABLE device_current_status (
                device TEXT PRIMARY KEY,
                status INTEGER NOT NULL,  -- 1 for on, 0 for off
                since DATETIME NOT NULL,  -- When the current status started
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    conn.commit()
    conn.close()
    
    if db_exists:
        print("✅ Database already existed, checked/created necessary tables")
    else:
        print("✅ Database newly created with all necessary tables")

# ========================= 
# save current data
# =========================
def save_to_db(soil, temp, hum, light, pressure):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_data (soil_moisture, temperature, humidity, light, pressure)
        VALUES (?, ?, ?, ?, ?)
    ''', (soil, temp, hum, light, pressure))
    print("✅ Inserted sensor data:", soil, temp, hum, light, pressure)
    conn.commit()
    conn.close()

def save_control_setting(pin, value):
    pin_descriptions = {
        "V8": "Smart Control",
        "V20": "Pump ON Threshold",
        "V21": "Fan Interval",
        "V22": "Lamp ON Threshold",
        "V23": "Pump OFF Threshold",
        "V24": "Lamp OFF Threshold",
        "V25": "Fan Duration"
    }
    
    description = pin_descriptions.get(pin, f"Unknown Pin {pin}")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Make sure tables exist
    if not check_table_exists(conn, "control_history"):
        cursor.execute('''
            CREATE TABLE control_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                pin TEXT NOT NULL,
                value REAL NOT NULL,
                description TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    if not check_table_exists(conn, "current_settings"):
        cursor.execute('''
            CREATE TABLE current_settings (
                pin TEXT PRIMARY KEY,
                value REAL NOT NULL,
                description TEXT,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    
    # Insert into control history
    cursor.execute('''
        INSERT INTO control_history (pin, value, description)
        VALUES (?, ?, ?)
    ''', (pin, value, description))
    
    # Update current settings
    cursor.execute('''
        REPLACE INTO current_settings (pin, value, description, updated_at)
        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
    ''', (pin, value, description))
    
    print(f"✅ Saved control setting: {description} ({pin}) = {value}")
    conn.commit()
    conn.close()

# ========================= 
# updating from Blynk 
# =========================
def collect_loop():
    while True:
        try:
            res = requests.get(BLYNK_API)
            data = res.json()
            print("📥 Received:", data)
            save_to_db(data["v1"], data["v2"], data["v3"], data["v6"], data["v10"])
            
            # Check if we need to perform smart control actions
            # (This would go here if implemented)
            
        except Exception as e:
            print("❌ Error:", e)
        
        # Sleep for 10 seconds before next data collection
        time.sleep(10)

# ========================= 
#  Flask 
# =========================
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

@app.route("/latest", methods=["GET", "OPTIONS"])
def get_latest():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT timestamp, soil_moisture, temperature, humidity, light, pressure FROM sensor_data ORDER BY id DESC LIMIT 1")
    except sqlite3.OperationalError:
        # Try with capital P if lowercase didn't work
        cursor.execute("SELECT timestamp, soil_moisture, temperature, humidity, light, Pressure FROM sensor_data ORDER BY id DESC LIMIT 1")
    
    row = cursor.fetchone()
    conn.close()
    
    if row:
        return jsonify({
            "timestamp": row[0],
            "soil": row[1],
            "temp": row[2],
            "humidity": row[3],
            "light": row[4],
            "pressure": row[5]  # Return as lowercase for consistency
        })
    return jsonify({"error": "No data"})

@app.route("/history", methods=["GET", "OPTIONS"])
def get_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT timestamp, soil_moisture, temperature, humidity, light, pressure FROM sensor_data ORDER BY id DESC LIMIT 50")
    except sqlite3.OperationalError:
        # Try with capital P if lowercase didn't work
        cursor.execute("SELECT timestamp, soil_moisture, temperature, humidity, light, Pressure FROM sensor_data ORDER BY id DESC LIMIT 50")
    
    rows = cursor.fetchall()
    conn.close()
    
    history = [
        {"timestamp": ts, "soil": s, "temp": t, "humidity": h, "light": l, "pressure": p}
        for ts, s, t, h, l, p in rows
    ]
    return jsonify(history)

@app.route("/stats", methods=["GET"])
def get_stats():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Get averages - handle both pressure column names
    try:
        # Try with lowercase first
        cursor.execute("""
            SELECT 
                AVG(soil_moisture) as avg_soil,
                AVG(temperature) as avg_temp,
                AVG(humidity) as avg_humidity,
                AVG(light) as avg_light,
                AVG(pressure) as avg_pressure,
                MAX(temperature) as max_temp,
                MIN(temperature) as min_temp,
                MAX(humidity) as max_humidity,
                MIN(humidity) as min_humidity
            FROM sensor_data
            WHERE timestamp >= datetime('now', '-24 hours')
        """)
    except sqlite3.OperationalError:
        # Try with capital P
        cursor.execute("""
            SELECT 
                AVG(soil_moisture) as avg_soil,
                AVG(temperature) as avg_temp,
                AVG(humidity) as avg_humidity,
                AVG(light) as avg_light,
                AVG(Pressure) as avg_pressure,
                MAX(temperature) as max_temp,
                MIN(temperature) as min_temp,
                MAX(humidity) as max_humidity,
                MIN(humidity) as min_humidity
            FROM sensor_data
            WHERE timestamp >= datetime('now', '-24 hours')
        """)
    
    stats = cursor.fetchone()
    conn.close()
    
    if stats:
        return jsonify({
            "avg_soil": round(stats[0], 1) if stats[0] else 0,
            "avg_temp": round(stats[1], 1) if stats[1] else 0,
            "avg_humidity": round(stats[2], 1) if stats[2] else 0,
            "avg_light": round(stats[3], 1) if stats[3] else 0,
            "avg_pressure": round(stats[4], 1) if stats[4] else 0,
            "max_temp": round(stats[5], 1) if stats[5] else 0,
            "min_temp": round(stats[6], 1) if stats[6] else 0,
            "max_humidity": round(stats[7], 1) if stats[7] else 0,
            "min_humidity": round(stats[8], 1) if stats[8] else 0
        })
    
    return jsonify({"error": "No data"})

# Get current settings
@app.route("/current-settings", methods=["GET"])
def get_current_settings():
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    if not check_table_exists(conn, "current_settings"):
        conn.close()
        return jsonify(DEFAULT_SETTINGS)
    
    cursor.execute("SELECT pin, value FROM current_settings")
    rows = cursor.fetchall()
    conn.close()
    
    settings = {row["pin"]: row["value"] for row in rows}
    
    # Fill in any missing settings with defaults
    for pin, default_value in DEFAULT_SETTINGS.items():
        if pin not in settings:
            settings[pin] = default_value
    
    return jsonify(settings)

# Set smart control parameters
@app.route("/set-smart-param", methods=["POST", "OPTIONS"])
def set_smart_param():
    print(f"🔔 Received request at /set-smart-param, method: {request.method}")
    
    if request.method == "OPTIONS":
        print("🔔 Handling OPTIONS request")
        return "", 200
    
    try:
        print("🔔 Trying to parse JSON data...")
        data = request.json
        print(f"🔔 Parsed JSON: {data}")
        
        pin = data.get("pin")
        value = data.get("value")
        
        if not pin or value is None:
            print("❌ Missing pin or value in request")
            return jsonify({"error": "Missing pin or value"}), 400
        
        print(f"🔔 Processing pin={pin}, value={value}")
        
        save_control_setting(pin, value)
        
        url = f"{BLYNK_WRITE_API}&{pin}={value}"
        
        print(f"🔔 Sending request to Blynk: {url}")
        
        response = requests.get(url)
        if response.status_code == 200:
            print(f"✅ Successfully set {pin} to {value}")
            return jsonify({"status": "success"})
        else:
            print(f"❌ Failed to set {pin} to {value}: {response.text}")
            return jsonify({"error": f"Blynk API error: {response.text}"}), 500
    except Exception as e:
        print(f"❌ Exception in set_smart_param: {str(e)}")
        return jsonify({"error": str(e)}), 500

# Get control history
@app.route("/control-history", methods=["GET", "OPTIONS"])
def get_control_history():
    limit = request.args.get('limit', 50, type=int)
    
    conn = sqlite3.connect(DB_FILE)
    
    if not check_table_exists(conn, "control_history"):
        conn.close()
        return jsonify([])  
    
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, pin, value, description, timestamp FROM control_history ORDER BY id DESC LIMIT ?", 
        (limit,)
    )
    rows = cursor.fetchall()
    conn.close()
    
    history = [dict(row) for row in rows]
    return jsonify(history)

@app.route("/control-device", methods=["POST"])
def control_device():
    try:
        data = request.json
        device = data.get("device")
        status = int(data.get("status"))
        reason = data.get("reason", "Manual control")

        if device not in ["pump", "lamp", "fan"]:
            return jsonify({"error": "Invalid device"}), 400
        if status not in [0, 1]:
            return jsonify({"error": "Invalid status"}), 400

        now = datetime.now().isoformat()  # use ISO 8601 format

        with get_safe_connection() as conn:
            cursor = conn.cursor()

            # 1. Update current status
            cursor.execute('''
                INSERT OR REPLACE INTO device_current_status (device, status, since, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
            ''', (device, status, now))

            # 2. Update operation history
            if status == 1:
                cursor.execute('''
                    INSERT INTO device_operation_history (device, status, start_time, reason)
                    VALUES (?, ?, ?, ?)
                ''', (device, status, now, reason))
            else:
                cursor.execute('''
                    SELECT id, start_time FROM device_operation_history
                    WHERE device = ? AND status = 1 AND end_time IS NULL
                    ORDER BY id DESC LIMIT 1
                ''', (device,))
                row = cursor.fetchone()
                if row:
                    op_id, start_time = row
                    start_dt = datetime.fromisoformat(start_time)
                    now_dt = datetime.fromisoformat(now)
                    duration = int((now_dt - start_dt).total_seconds())
                    cursor.execute('''
                        UPDATE device_operation_history
                        SET end_time = ?, duration = ?
                        WHERE id = ?
                    ''', (now, duration, op_id))
            # send to Blynk
            device_to_pin = {
                "pump": "V4",
                "lamp": "V11",
                "fan":  "V7"
            }

            blynk_pin = device_to_pin.get(device)
            if blynk_pin:
                blynk_url = f"{BLYNK_WRITE_API}&{blynk_pin}={status}"
                try:
                    blynk_response = requests.get(blynk_url)
                    print(f"📤 Sent to Blynk: {blynk_url}, Response: {blynk_response.status_code}")
                except Exception as e:
                    print(f"❌ Failed to update Blynk pin {blynk_pin}: {e}")

            conn.commit()

        print(f"✅ Updated {device} status to {status}")
        return jsonify({"status": "success", "device": device, "new_status": status})

    except Exception as e:
        print(f"❌ Exception in control_device: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/device-history", methods=["GET"])
def get_device_history():
    try:
        device = request.args.get("device")
        status = request.args.get("status")
        reason = request.args.get("reason")
        start_date = request.args.get("start_date")
        end_date = request.args.get("end_date")
        sort = request.args.get("sort", "start_time")
        order = request.args.get("order", "desc")

        with get_safe_connection() as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            query = "SELECT * FROM device_operation_history WHERE 1=1"
            params = []

            if device:
                query += " AND device = ?"
                params.append(device)
            if status is not None and status != "":
                query += " AND status = ?"
                params.append(int(status))
            if reason:
                query += " AND reason LIKE ?"
                params.append(f"%{reason}%")
            if start_date and end_date:
                query += " AND start_time BETWEEN ? AND ?"
                params.append(start_date)
                params.append(end_date)

            if sort not in ["device", "status", "start_time", "end_time", "duration", "reason"]:
                sort = "start_time"
            if order.lower() not in ["asc", "desc"]:
                order = "desc"
            query += f" ORDER BY {sort} {order.upper()}"

            cursor.execute(query, params)
            rows = cursor.fetchall()
            result = [dict(row) for row in rows]
            return jsonify(result)

    except Exception as e:
        print("❌ Error in /device-history:", e)
        return jsonify({"error": str(e)}), 500

@app.route("/device-status", methods=["GET"])
def get_device_status():
    try:
        with get_safe_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT device, status FROM device_current_status")
            rows = cursor.fetchall()
        devices = [{"device": row[0], "status": row[1]} for row in rows]
        return jsonify({"devices": devices})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/")
def home():
    return "✅ Flask backend is running!"

# CORS
@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response

# ========================= 
# main app
# =========================
if __name__ == "__main__":
    init_db()
    
    collector_thread = threading.Thread(target=collect_loop, daemon=True)
    collector_thread.start()
    
    # start Flask
    print("🚀 Starting Flask server on http://localhost:5050")
    app.run(debug=True, port=5050, host="0.0.0.0")