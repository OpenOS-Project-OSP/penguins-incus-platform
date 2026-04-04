import React from "react";

const COLORS: Record<string, string> = {
  Running:  "#22c55e",
  Stopped:  "#94a3b8",
  Frozen:   "#60a5fa",
  Error:    "#ef4444",
  Unknown:  "#f59e0b",
  Online:   "#22c55e",
  Offline:  "#ef4444",
  Evacuated:"#f59e0b",
  succeeded:"#22c55e",
  failed:   "#ef4444",
  running:  "#60a5fa",
  pending:  "#f59e0b",
  cancelled:"#94a3b8",
};

interface Props { status: string; }

export const StatusBadge: React.FC<Props> = ({ status }) => (
  <span style={{
    display: "inline-flex", alignItems: "center", gap: 4,
    fontSize: 12, fontWeight: 500,
    color: COLORS[status] ?? "#94a3b8",
  }}>
    <span style={{
      width: 8, height: 8, borderRadius: "50%",
      background: COLORS[status] ?? "#94a3b8",
      flexShrink: 0,
    }} />
    {status}
  </span>
);
