import React from "react";

export default function NotificationSettings() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-semibold mb-4">Notification Settings</h1>

      {/* Заглушка: сюда позже добавим форму порогов и каналов */}
      <div className="rounded-lg border border-gray-200 p-4 text-gray-600">
        Здесь будут настраиваться пороги оповещений, каналы (push, Telegram и т. д.) и расписание.
      </div>
    </div>
  );
}