import { useEffect } from "react";

/**
 * useAlerts - polls backend /alerts and shows simple pop-up notifications.
 * @param {number} interval Polling interval in milliseconds. Default 10000 (10 sec).
 */
export default function useAlerts(interval = 10000) {
  useEffect(() => {
    // Polling function
    const checkAlerts = () => {
      fetch("/alerts")
        .then((res) => res.json())
        .then((data) => {
          if (Array.isArray(data) && data.length > 0) {
            data.forEach(({ type, message }) => {
              // Simple alert - can be replaced with toast later
              window.alert(message);
            });
          }
        })
        .catch((err) => {
          console.error("Error fetching alerts:", err);
        });
    };

    // First call immediately on mount
    checkAlerts();
    // And repeat every interval milliseconds
    const timerId = setInterval(checkAlerts, interval);

    // Cleanup on unmount
    return () => clearInterval(timerId);
  }, [interval]);
}