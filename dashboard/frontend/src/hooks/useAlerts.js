import { useEffect } from "react";

/**
 * useAlerts — опрашивает бэкэнд /alerts и показывает простые всплывашки.
 * @param {number} interval Интервал опроса в миллисекундах. По умолчанию 10000 (10 сек).
 */
export default function useAlerts(interval = 10000) {
  useEffect(() => {
    // Функция опроса
    const checkAlerts = () => {
      fetch("/alerts")
        .then((res) => res.json())
        .then((data) => {
          if (Array.isArray(data) && data.length > 0) {
            data.forEach(({ type, message }) => {
              // просто alert — позже можно заменить на toast
              window.alert(message);
            });
          }
        })
        .catch((err) => {
          console.error("Error fetching alerts:", err);
        });
    };

    // первый вызов сразу при монтировании
    checkAlerts();
    // и повторять каждые interval миллисекунд
    const timerId = setInterval(checkAlerts, interval);

    // очистка при демонтировании
    return () => clearInterval(timerId);
  }, [interval]);
}