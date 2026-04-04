import React, { useCallback } from "react";
import { api, Operation } from "../api/client";
import { useApi } from "../hooks/useApi";
import { useEvents } from "../hooks/useEvents";
import { StatusBadge } from "../components/StatusBadge";
import { PageHeader } from "../components/PageHeader";

const fmt = (iso?: string) => iso ? new Date(iso).toLocaleString() : "—";

export const OperationsPage: React.FC = () => {
  const { data, loading, error, reload } = useApi(() => api.listOperations(), []);
  useEvents(useCallback((e) => { if (e.type === "operation") reload(); }, [reload]));
  const ops: Operation[] = data ?? [];
  const cancel = async (id: string) => { try { await api.cancelOperation(id); reload(); } catch { /* ignore */ } };
  return (
    <div style={{ padding:24 }}>
      <PageHeader title="Operations" onRefresh={reload} />
      {loading && <p style={{ color:"#888" }}>Loading…</p>}
      {error   && <p style={{ color:"#ef4444" }}>Error: {error}</p>}
      {!loading && !error && (
        <table style={{ width:"100%",borderCollapse:"collapse",fontSize:14 }}>
          <thead><tr style={{ borderBottom:"2px solid #e5e7eb",textAlign:"left" }}>
            {["ID","Description","Status","Created","Actions"].map(h=><th key={h} style={{ padding:"8px 12px",fontWeight:600,color:"#374151" }}>{h}</th>)}
          </tr></thead>
          <tbody>
            {ops.length===0 && <tr><td colSpan={5} style={{ padding:24,textAlign:"center",color:"#9ca3af" }}>No operations</td></tr>}
            {ops.map(op=>(
              <tr key={op.id} style={{ borderBottom:"1px solid #f3f4f6" }}>
                <td style={{ padding:"10px 12px",fontFamily:"monospace",fontSize:12 }}>{op.id.slice(0,8)}…</td>
                <td style={{ padding:"10px 12px" }}>{op.description}</td>
                <td style={{ padding:"10px 12px" }}><StatusBadge status={op.status} /></td>
                <td style={{ padding:"10px 12px",color:"#6b7280",fontSize:13 }}>{fmt(op.created_at)}</td>
                <td style={{ padding:"10px 12px" }}>
                  {(op.status==="running"||op.status==="pending") && (
                    <button onClick={()=>cancel(op.id)} style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"none",background:"#ef4444",color:"#fff",cursor:"pointer" }}>Cancel</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
