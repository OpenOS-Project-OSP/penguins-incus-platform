import { useEffect } from "react";
import { api, KimEvent } from "../api/client";

/** Subscribe to the daemon SSE event stream. Calls onEvent for each message. */
export function useEvents(
  onEvent: (e: KimEvent) => void,
  type = "",
  project = ""
): void {
  useEffect(() => {
    const es = api.eventSource(type, project);
    es.onmessage = (msg) => {
      try { onEvent(JSON.parse(msg.data) as KimEvent); }
      catch { /* ignore malformed */ }
    };
    return () => es.close();
  }, [type, project, onEvent]);
}
