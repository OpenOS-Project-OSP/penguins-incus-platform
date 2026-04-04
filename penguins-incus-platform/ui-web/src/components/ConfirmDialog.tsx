import React from "react";

interface Props {
  open: boolean;
  title: string;
  message: string;
  confirmLabel?: string;
  onConfirm: () => void;
  onCancel: () => void;
}

export const ConfirmDialog: React.FC<Props> = ({
  open, title, message, confirmLabel = "Confirm", onConfirm, onCancel,
}) => {
  if (!open) return null;
  return (
    <div style={{
      position: "fixed", inset: 0, background: "rgba(0,0,0,.4)",
      display: "flex", alignItems: "center", justifyContent: "center", zIndex: 1000,
    }}>
      <div style={{
        background: "#fff", borderRadius: 8, padding: 24, minWidth: 320,
        boxShadow: "0 8px 32px rgba(0,0,0,.2)",
      }}>
        <h3 style={{ margin: "0 0 8px" }}>{title}</h3>
        <p style={{ margin: "0 0 20px", color: "#555" }}>{message}</p>
        <div style={{ display: "flex", gap: 8, justifyContent: "flex-end" }}>
          <button onClick={onCancel}
            style={{ padding: "6px 16px", borderRadius: 4, border: "1px solid #ddd", cursor: "pointer" }}>
            Cancel
          </button>
          <button onClick={onConfirm}
            style={{ padding: "6px 16px", borderRadius: 4, border: "none",
                     background: "#ef4444", color: "#fff", cursor: "pointer" }}>
            {confirmLabel}
          </button>
        </div>
      </div>
    </div>
  );
};
