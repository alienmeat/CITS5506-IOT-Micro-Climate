import React from "react";

/**
 * ToggleSwitch — компактный тумблер.
 * props:
 *   • label    — строка подписи
 *   • checked  — boolean
 *   • onChange — (bool) => void
 */
export default function ToggleSwitch({ checked, onChange, label }) {
  return (
    <div className="flex justify-between items-center w-full">
      <span className="text-sm text-gray-700 select-none">{label}</span>

      <label className="inline-flex items-center cursor-pointer">
        <input
          type="checkbox"
          className="sr-only peer"
          checked={checked}
          onChange={(e) => onChange(e.target.checked)}
        />
        <div className="w-10 h-6 bg-gray-400 peer-checked:bg-blue-500 rounded-full relative transition-colors">
          <div
            className="absolute top-1 left-1 w-4 h-4 bg-white rounded-full
                       transition-transform peer-checked:translate-x-4"
          />
        </div>
      </label>
    </div>
  );
}