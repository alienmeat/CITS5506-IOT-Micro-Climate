from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import threading
import requests
import time

# =========================
# 🗃️ 初始化数据库
# =========================
DB_FILE = "blynk_data.db"
BLYNK_TOKEN = "FpQ6nvN9nATbU1E6qNbcfqU5XMmlYQI3"
BLYNK_API = f"https://blynk.cloud/external/api/get?token={BLYNK_TOKEN}&v1&v2&v3&v6"

def init_db():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            soil_moisture REAL,
            temperature REAL,
            humidity REAL,
            light REAL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

# =========================
# 💾 保存数据
# =========================
def save_to_db(soil, temp, hum, light):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO sensor_data (soil_moisture, temperature, humidity, light)
        VALUES (?, ?, ?, ?)
    ''', (soil, temp, hum, light))
    print("✅ Inserted:", soil, temp, hum, light)
    conn.commit()
    conn.close()

# =========================
# 🔄 定时采集数据（后台运行）
# =========================
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

# =========================
# 🌐 Flask 接口部分
# =========================
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route("/latest")
def get_latest():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, soil_moisture, temperature, humidity, light FROM sensor_data ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    conn.close()

    if row:
        return jsonify({
            "timestamp": row[0],
            "soil": row[1],
            "temp": row[2],
            "humidity": row[3],
            "light": row[4]
        })
    return jsonify({"error": "No data"})

@app.route("/history")
def get_history():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp, soil_moisture, temperature, humidity, light FROM sensor_data ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()

    history = [
        {"timestamp": ts, "soil": s, "temp": t, "humidity": h, "light": l}
        for ts, s, t, h, l in rows
    ]
    return jsonify(history)

@app.route("/")
def home():
    return "✅ Flask backend is running!"

# =========================
# 🚀 主程序入口
# =========================
if __name__ == "__main__":
    init_db()

    # 启动采集线程
    collector_thread = threading.Thread(target=collect_loop, daemon=True)
    collector_thread.start()

    # 启动 Flask
    app.run(debug=True, port=5000)


# from flask import Flask, jsonify
# from flask_cors import CORS
# import sqlite3

# # db_init.py
# def init_db():
#     conn = sqlite3.connect("blynk_data.db")
#     cursor = conn.cursor()
#     cursor.execute('''
#         CREATE TABLE IF NOT EXISTS sensor_data (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             soil_moisture REAL,
#             temperature REAL,
#             humidity REAL,
#             light REAL,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     ''')
#     conn.commit()
#     conn.close()

# # 创建 Flask 应用
# app = Flask(__name__)

# # ✅ 关键配置：允许所有来源访问所有路由（彻底解决 CORS）
# # CORS(app, resources={r"/*": {"origins": "*"}})

# # AMB
# # CORS(app, supports_credentials=True, origins="*")
# CORS(app, origins=["http://localhost:3000"])


# # 数据库文件
# DB_FILE = "blynk_data.db"

# # ✅ 接口 1：获取最新一条记录
# @app.route("/latest")
# def get_latest():
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT timestamp, soil_moisture, temperature, humidity, light FROM sensor_data ORDER BY id DESC LIMIT 1")
#     row = cursor.fetchone()
#     conn.close()

#     if row:
#         return jsonify({
#             "timestamp": row[0],
#             "soil": row[1],
#             "temp": row[2],
#             "humidity": row[3],
#             "light": row[4]
#         })
#     return jsonify({"error": "No data"})

# # ✅ 接口 2：获取最近 50 条历史数据（用于图表）
# @app.route("/history")
# def get_history():
#     conn = sqlite3.connect(DB_FILE)
#     cursor = conn.cursor()
#     cursor.execute("SELECT timestamp, soil_moisture, temperature, humidity, light FROM sensor_data ORDER BY id DESC LIMIT 50")
#     rows = cursor.fetchall()
#     conn.close()

#     history = [
#         {"timestamp": ts, "soil": s, "temp": t, "humidity": h, "light": l}
#         for ts, s, t, h, l in rows
#     ]
#     return jsonify(history)

# # ✅ 可选首页测试接口
# @app.route("/")
# def home():
#     return "✅ Flask backend is running!"

# # ✅ 启动 Flask 服务
# if __name__ == "__main__":
#     app.run(debug=True, port=5000)