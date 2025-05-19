
import { useEffect } from "react";

/**
 * useAlerts — опрашивает backend /alerts и показывает простые pop-up уведомления.
 * @param {number} interval — интервал в мс (по умолчанию 10000).
 */
export default function useAlerts(interval = 10000) {
  useEffect(() => {
    const checkAlerts = () => {
      fetch("/alerts")
        .then((res) => res.json())
        .then((data) => {
          if (Array.isArray(data) && data.length > 0) {
            data.forEach((evt) => {
              window.alert(evt.message);
            });
          }
        })
        .catch((err) => {
          console.error("Error fetching alerts:", err);
        });
    };

    // первый вызов сразу
    checkAlerts();
    // периодический
    const id = setInterval(checkAlerts, interval);
    return () => clearInterval(id);
  }, [interval]);
}
