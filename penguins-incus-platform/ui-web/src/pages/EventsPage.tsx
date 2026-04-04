import React, { useCallback, useRef, useState } from "react";
import { KimEvent } from "../api/client";
import { useEvents } from "../hooks/useEvents";
import { PageHeader } from "../components/PageHeader";

const MAX_EVENTS = 200;

export const EventsPage: React.FC = () => {
  const [events, setEvents] = useState<KimEvent[]>([]);
  const [filter, setFilter] = useState("");
  const [paused, setPaused] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEvents(useCallback((e: KimEvent) => {
    if (paused) return;
    setEvents(prev => {
      const next = [...prev, e];
      return next.length > MAX_EVENTS ? next.slice(-MAX_EVENTS) : next;
    });
    setTimeout(() => bottomRef.current?.scrollIntoView({ behavior: "smooth" }), 50);
  }, [paused]));

  const filtered = filter
    ? events.filter(e => e.type.includes(filter) || JSON.stringify(e.metadata).includes(filter))
    : events;

  return (
    <div style={{ padding:24, display:"flex", flexDirection:"column", height:"100%" }}>
      <PageHeader title="Events"
        action={
          <div style={{ display:"flex",gap:8,alignItems:"center" }}>
            <input value={filter} onChange={e=>setFilter(e.target.value)}
              placeholder="Filter…"
              style={{ padding:"5px 10px",borderRadius:4,border:"1px solid #ddd",fontSize:13 }} />
            <button onClick={()=>setPaused(p=>!p)}
              style={{ padding:"6px 12px",borderRadius:4,border:"1px solid #ddd",cursor:"pointer",
                       background:paused?"#fef9c3":"#fff" }}>
              {paused?"▶ Resume":"⏸ Pause"}
            </button>
            <button onClick={()=>setEvents([])}
              style={{ padding:"6px 12px",borderRadius:4,border:"1px solid #ddd",cursor:"pointer" }}>
              Clear
            </button>
          </div>
        }
      />
      <div style={{ flex:1,overflow:"auto",background:"#0f172a",borderRadius:8,
                    padding:12,fontFamily:"monospace",fontSize:12,color:"#e2e8f0" }}>
        {filtered.length===0 && (
          <span style={{ color:"#475569" }}>Waiting for events…</span>
        )}
        {filtered.map((e, i) => (
          <div key={i} style={{ marginBottom:4,borderBottom:"1px solid #1e293b",paddingBottom:4 }}>
            <span style={{ color:"#94a3b8",marginRight:8 }}>{e.timestamp||"—"}</span>
            <span style={{ color:"#60a5fa",marginRight:8 }}>[{e.type}]</span>
            {e.project && <span style={{ color:"#a78bfa",marginRight:8 }}>{e.project}</span>}
            <span style={{ color:"#e2e8f0" }}>{JSON.stringify(e.metadata)}</span>
          </div>
        ))}
        <div ref={bottomRef} />
      </div>
    </div>
  );
};
