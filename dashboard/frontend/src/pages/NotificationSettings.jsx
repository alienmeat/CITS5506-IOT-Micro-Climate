import React, { useState } from "react";
import RangeSlider from "../components/ui/RangeSlider";

export default function NotificationSettings() {
  const [tempRange, setTempRange] = useState([10, 35]);      // °C
  const [humidRange, setHumidRange] = useState([30, 70]);    // %
  const [pressRange, setPressRange] = useState([980, 1020]); // hPa

  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Notification Settings</h1>

      <div className="space-y-6">
        <RangeSlider
          label="Air Temperature (°C)"
          min={0}
          max={50}
          step={1}
          values={tempRange}
          onChange={setTempRange}
        />

        <RangeSlider
          label="Air Humidity (%)"
          min={0}
          max={100}
          step={1}
          values={humidRange}
          onChange={setHumidRange}
        />

        <RangeSlider
          label="Atmospheric Pressure (hPa)"
          min={930}
          max={1060}
          step={1}
          values={pressRange}
          onChange={setPressRange}
        />
      </div>
    </div>
  );
}