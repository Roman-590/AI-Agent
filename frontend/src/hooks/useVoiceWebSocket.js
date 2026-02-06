import { useCallback, useEffect, useRef, useState } from "react";

export default function useVoiceWebSocket(url) {
  const socketRef = useRef(null);
  const [lastEvent, setLastEvent] = useState(null);

  useEffect(() => {
    const socket = new WebSocket(url);
    socketRef.current = socket;

    socket.addEventListener("message", (event) => {
      try {
        const data = JSON.parse(event.data);
        setLastEvent(data);
      } catch (error) {
        console.error("Invalid message", error);
      }
    });

    return () => {
      socket.close();
    };
  }, [url]);

  const sendEvent = useCallback((payload) => {
    if (!socketRef.current || socketRef.current.readyState !== WebSocket.OPEN) {
      return;
    }
    socketRef.current.send(JSON.stringify(payload));
  }, []);

  return { sendEvent, lastEvent };
}
