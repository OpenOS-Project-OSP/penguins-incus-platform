import React from "react";
import { api, ClusterMember } from "../api/client";
import { useApi } from "../hooks/useApi";
import { StatusBadge } from "../components/StatusBadge";
import { PageHeader } from "../components/PageHeader";

export const ClusterPage: React.FC = () => {
  const { data, loading, error, reload } = useApi(() => api.listClusterMembers(), []);
  const members: ClusterMember[] = data ?? [];
  const act = async (fn: () => Promise<unknown>) => { try { await fn(); reload(); } catch { /* ignore */ } };
  return (
    <div style={{ padding:24 }}>
      <PageHeader title="Cluster" onRefresh={reload} />
      {loading && <p style={{ color:"#888" }}>Loading…</p>}
      {error   && <p style={{ color:"#ef4444" }}>Error: {error}</p>}
      {!loading && !error && (
        <table style={{ width:"100%",borderCollapse:"collapse",fontSize:14 }}>
          <thead><tr style={{ borderBottom:"2px solid #e5e7eb",textAlign:"left" }}>
            {["Name","URL","Status","Roles","Architecture","Actions"].map(h=><th key={h} style={{ padding:"8px 12px",fontWeight:600,color:"#374151" }}>{h}</th>)}
          </tr></thead>
          <tbody>
            {members.length===0 && <tr><td colSpan={6} style={{ padding:24,textAlign:"center",color:"#9ca3af" }}>No cluster members (standalone mode)</td></tr>}
            {members.map(m=>(
              <tr key={m.name} style={{ borderBottom:"1px solid #f3f4f6" }}>
                <td style={{ padding:"10px 12px",fontWeight:500 }}>{m.name}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280",fontSize:12,fontFamily:"monospace" }}>{m.url}</td>
                <td style={{ padding:"10px 12px" }}><StatusBadge status={m.status} /></td>
                <td style={{ padding:"10px 12px",color:"#6b7280",fontSize:13 }}>{m.roles?.join(", ")||"—"}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280" }}>{m.architecture||"—"}</td>
                <td style={{ padding:"10px 12px" }}>
                  <div style={{ display:"flex",gap:4 }}>
                    {m.status==="Online" && <button onClick={()=>act(()=>api.evacuateClusterMember(m.name))} style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"1px solid #ddd",cursor:"pointer" }}>Evacuate</button>}
                    {m.status==="Evacuated" && <button onClick={()=>act(()=>api.restoreClusterMember(m.name))} style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"1px solid #ddd",cursor:"pointer" }}>Restore</button>}
                    <button onClick={()=>act(()=>api.removeClusterMember(m.name))} style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"none",background:"#ef4444",color:"#fff",cursor:"pointer" }}>Remove</button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};
