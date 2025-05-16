// ✅ Dashboard.jsx：加入 Chart.js 折线图展示历史温湿度数据
import React, { useEffect, useState } from "react";
import { Card, CardContent } from "../components/ui/card";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const API_LATEST = "http://127.0.0.1:5000/latest";
const API_HISTORY = "http://127.0.0.1:5000/history";

function formatLocalTime(utcString) {
  if (!utcString || utcString === "--") return "--";
  const isoString = utcString.replace(" ", "T") + "Z";
  const date = new Date(isoString);
  return date.toLocaleString("en-AU", {
    timeZone: "Australia/Perth",
    hour12: false,
  });
}

export default function Dashboard() {
  const [data, setData] = useState({
    timestamp: "--",
    soil: "--",
    temp: "--",
    humidity: "--",
    light: "--",
  });

  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await fetch(API_LATEST);
        const json = await res.json();
        setData(json);
      } catch (error) {
        console.error("❌ 获取 Flask 最新数据失败：", error);
      }
    };

    const fetchHistory = async () => {
      try {
        const res = await fetch(API_HISTORY);
        const json = await res.json();
        setHistory(json.reverse()); // 保证时间顺序
      } catch (error) {
        console.error("❌ 获取 Flask 历史数据失败：", error);
      }
    };

    fetchData();
    fetchHistory();
    const interval = setInterval(() => {
      fetchData();
      fetchHistory();
    }, 5000);

    return () => clearInterval(interval);
  }, []);

  const summaryData = [
    { label: "Soil Moisture", value: `${data.soil} %` },
    { label: "Temperature", value: `${data.temp} °C` },
    { label: "Humidity", value: `${data.humidity} %` },
    { label: "Light", value: data.light },
  ];

  const chartData = {
    labels: history.map((d) => formatLocalTime(d.timestamp)),
    datasets: [
      {
        label: "Temperature (°C)",
        data: history.map((d) => d.temp),
        borderColor: "#5D5FEF",
        backgroundColor: "rgba(93, 95, 239, 0.2)",
        tension: 0.4,
      },
      {
        label: "Humidity (%)",
        data: history.map((d) => d.humidity),
        borderColor: "#7ED6DF",
        backgroundColor: "rgba(126, 214, 223, 0.2)",
        tension: 0.4,
      },
    ],
  };

  return (
    <div className="min-h-screen bg-[#f4f7fe] p-6">
      <h1 className="text-2xl font-bold mb-6">Smart Garden Dashboard</h1>
      <p className="text-sm text-gray-500 mb-4">
        Last updated: {formatLocalTime(data.timestamp)}
      </p>
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        {summaryData.map((item, index) => (
          <Card key={index} className="rounded-2xl shadow-sm">
            <CardContent className="p-4">
              <p className="text-sm text-gray-500">{item.label}</p>
              <p className="text-2xl font-bold text-gray-800">{item.value}</p>
            </CardContent>
          </Card>
        ))}
      </div>
      <Card className="rounded-2xl shadow-sm">
        <CardContent className="p-4">
          <h2 className="text-lg font-semibold text-gray-700 mb-2">Temperature & Humidity Trends</h2>
          <Line data={chartData} />
        </CardContent>
      </Card>
    </div>
  );
}