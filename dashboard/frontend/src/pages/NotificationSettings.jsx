import React, { useState } from "react";
import RangeSlider from "../components/ui/RangeSlider";
import ToggleSwitch from "../components/ui/ToggleSwitch";

export default function NotificationSettings() {
  /* диапазоны порогов */
  const [tempRange, setTempRange] = useState([10, 35]);
  const [humidRange, setHumidRange] = useState([30, 70]);
  const [pressRange, setPressRange] = useState([980, 1020]);

  /* тумблеры уведомлений */
  const [alerts, setAlerts] = useState({
    cold: true,
    heat: true,
    dry: true,
    humid: true,
    lowPress: true,
    highPress: true,
  });
  const toggle = (key) => (val) => setAlerts((s) => ({ ...s, [key]: val }));

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <h1 className="text-2xl font-semibold mb-6">Notification Settings</h1>

      <div className="space-y-8">
        {/* ── Temperature ───────────────────────────── */}
        <div className="grid grid-cols-[1fr_12rem] gap-6 items-stretch">
          <RangeSlider
            label="Air Temperature (°C)"
            min={0}
            max={50}
            step={1}
            values={tempRange}
            onChange={setTempRange}
          />

          <div className="bg-white rounded shadow p-4 flex flex-col justify-between gap-4 h-full">
            <ToggleSwitch
              label="Cold alert"
              checked={alerts.cold}
              onChange={toggle("cold")}
            />
            <ToggleSwitch
              label="Heat alert"
              checked={alerts.heat}
              onChange={toggle("heat")}
            />
          </div>
        </div>

        {/* ── Humidity ──────────────────────────────── */}
        <div className="grid grid-cols-[1fr_12rem] gap-6 items-stretch">
          <RangeSlider
            label="Air Humidity (%)"
            min={0}
            max={100}
            step={1}
            values={humidRange}
            onChange={setHumidRange}
          />

          <div className="bg-white rounded shadow p-4 flex flex-col justify-between gap-4 h-full">
            <ToggleSwitch
              label="Dry air alert"
              checked={alerts.dry}
              onChange={toggle("dry")}
            />
            <ToggleSwitch
              label="Humid air alert"
              checked={alerts.humid}
              onChange={toggle("humid")}
            />
          </div>
        </div>

        {/* ── Pressure ─────────────────────────────── */}
        <div className="grid grid-cols-[1fr_12rem] gap-6 items-stretch">
          <RangeSlider
            label="Atmospheric Pressure (hPa)"
            min={930}
            max={1060}
            step={1}
            values={pressRange}
            onChange={setPressRange}
          />

          <div className="bg-white rounded shadow p-4 flex flex-col justify-between gap-4 h-full">
            <ToggleSwitch
              label="Low pressure"
              checked={alerts.lowPress}
              onChange={toggle("lowPress")}
            />
            <ToggleSwitch
              label="High pressure"
              checked={alerts.highPress}
              onChange={toggle("highPress")}
            />
          </div>
        </div>
      </div>
    </div>
  );
}