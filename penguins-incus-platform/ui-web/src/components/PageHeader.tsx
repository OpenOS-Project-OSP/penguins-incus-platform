import React from "react";

interface Props {
  title: string;
  action?: React.ReactNode;
  onRefresh?: () => void;
}

export const PageHeader: React.FC<Props> = ({ title, action, onRefresh }) => (
  <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between",
                marginBottom: 20 }}>
    <h2 style={{ margin: 0, fontSize: 20, fontWeight: 600 }}>{title}</h2>
    <div style={{ display: "flex", gap: 8 }}>
      {onRefresh && (
        <button onClick={onRefresh}
          style={{ padding: "6px 12px", borderRadius: 4, border: "1px solid #ddd",
                   cursor: "pointer", background: "#fff" }}>
          ↻ Refresh
        </button>
      )}
      {action}
    </div>
  </div>
);
