# 🌿 Smart Garden Dashboard

An IoT-enabled smart garden monitoring system that collects real-time sensor data from an ESP32 via Blynk Cloud, stores it using a Flask + SQLite backend, and visualizes it in a professional React + TailwindCSS dashboard.

---

## 📦 Project Structure

```
CITS5506-IOT-Micro-Climate/
├── backend/              # Flask + SQLite backend
│   ├── app.py            # API endpoints (/latest, /history)
│   ├── blynk_logger.py   # Periodically fetches data from Blynk and saves to SQLite
│   ├── blynk_data.db     # Local SQLite database (ignored via .gitignore)
│   └── venv/             # Python virtual environment (ignored)
├── frontend/             # React + Tailwind dashboard
│   ├── src/              # Main UI (Dashboard.jsx)
│   └── node_modules/     # npm packages (ignored)
└── .gitignore
```

---

## 🛠️ Technologies Used

| Layer        | Tech Stack                               |
|--------------|-------------------------------------------|
| Microcontroller | XIAO ESP32 (or ESP32) + Blynk Cloud       |
| Backend      | Python 3, Flask, SQLite, flask-cors       |
| Frontend     | React, TailwindCSS, Chart.js              |
| Deployment   | GitHub (local dev setup)                  |

---

## 🚀 Getting Started

### ✅ 1. Backend Setup

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py        # Starts Flask server at http://localhost:5000
```

In another terminal:

```bash
python blynk_logger.py  # Starts data collection every 10 seconds
```

### ✅ 2. Frontend Setup

```bash
cd frontend
npm install
npm start               # Opens React dashboard at http://localhost:3000
```

---

## 📈 Dashboard Features

- Real-time display of:
  - Soil moisture
  - Temperature
  - Humidity
  - Light
- Auto-updating data (5s interval)
- Historical line chart (temperature + humidity trends)

---

## 🔒 .gitignore Highlights

- Ignores `node_modules/`, `venv/`, and `.db` files
- Clean and light Git history

---

## 📌 To-Do

- [ ] Add pump control via Blynk (V4)
- [ ] Add alert thresholds for moisture
- [ ] Export CSV download of history
- [ ] Deploy backend with gunicorn or Flask serverless

---

## 👩‍💻 Author

Created by [Your Name], for **CITS5506 Internet of Things (UWA)**  
Feel free to fork, clone, and build upon!
