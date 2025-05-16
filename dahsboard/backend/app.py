from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3

# 创建 Flask 应用
app = Flask(__name__)

# ✅ 关键配置：允许所有来源访问所有路由（彻底解决 CORS）
CORS(app, resources={r"/*": {"origins": "*"}})

# 数据库文件
DB_FILE = "blynk_data.db"

# ✅ 接口 1：获取最新一条记录
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

# ✅ 接口 2：获取最近 50 条历史数据（用于图表）
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

# ✅ 可选首页测试接口
@app.route("/")
def home():
    return "✅ Flask backend is running!"

# ✅ 启动 Flask 服务
if __name__ == "__main__":
    app.run(debug=True, port=5000)