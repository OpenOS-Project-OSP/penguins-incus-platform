import React, { useState } from "react";
import { api, Network } from "../api/client";
import { useApi } from "../hooks/useApi";
import { PageHeader } from "../components/PageHeader";
import { ConfirmDialog } from "../components/ConfirmDialog";

const CreateNetworkDialog: React.FC<{ onClose: () => void; onCreated: () => void }> = ({ onClose, onCreated }) => {
  const [name, setName] = useState(""); const [type, setType] = useState("bridge");
  const [error, setError] = useState(""); const [busy, setBusy] = useState(false);
  const submit = async () => {
    if (!name.trim()) { setError("Name is required"); return; }
    setBusy(true);
    try { await api.createNetwork({ name, type }); onCreated(); onClose(); }
    catch (e) { setError((e as Error).message); } finally { setBusy(false); }
  };
  return (
    <div style={{ position:"fixed",inset:0,background:"rgba(0,0,0,.4)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:1000 }}>
      <div style={{ background:"#fff",borderRadius:8,padding:24,minWidth:360,boxShadow:"0 8px 32px rgba(0,0,0,.2)" }}>
        <h3 style={{ margin:"0 0 16px" }}>Create Network</h3>
        <label style={{ display:"block",marginBottom:12 }}>
          <span style={{ fontSize:13,color:"#555" }}>Name</span>
          <input value={name} onChange={e=>setName(e.target.value)} style={{ display:"block",width:"100%",marginTop:4,padding:"6px 8px",border:"1px solid #ddd",borderRadius:4,boxSizing:"border-box" }} />
        </label>
        <label style={{ display:"block",marginBottom:16 }}>
          <span style={{ fontSize:13,color:"#555" }}>Type</span>
          <select value={type} onChange={e=>setType(e.target.value)} style={{ display:"block",width:"100%",marginTop:4,padding:"6px 8px",border:"1px solid #ddd",borderRadius:4 }}>
            {["bridge","macvlan","sriov","ovn","physical"].map(t=><option key={t}>{t}</option>)}
          </select>
        </label>
        {error && <p style={{ color:"#ef4444",margin:"0 0 12px",fontSize:13 }}>{error}</p>}
        <div style={{ display:"flex",gap:8,justifyContent:"flex-end" }}>
          <button onClick={onClose} disabled={busy} style={{ padding:"6px 16px",borderRadius:4,border:"1px solid #ddd",cursor:"pointer" }}>Cancel</button>
          <button onClick={submit} disabled={busy} style={{ padding:"6px 16px",borderRadius:4,border:"none",background:"#1a73e8",color:"#fff",cursor:"pointer" }}>{busy?"Creating…":"Create"}</button>
        </div>
      </div>
    </div>
  );
};

export const NetworksPage: React.FC = () => {
  const { data, loading, error, reload } = useApi(() => api.listNetworks(), []);
  const [showCreate, setShowCreate] = useState(false);
  const [confirm, setConfirm] = useState<Network | null>(null);
  const networks: Network[] = data ?? [];
  return (
    <div style={{ padding:24 }}>
      <PageHeader title="Networks" onRefresh={reload}
        action={<button onClick={()=>setShowCreate(true)} style={{ padding:"6px 16px",borderRadius:4,border:"none",background:"#1a73e8",color:"#fff",cursor:"pointer" }}>+ Create</button>} />
      {loading && <p style={{ color:"#888" }}>Loading…</p>}
      {error   && <p style={{ color:"#ef4444" }}>Error: {error}</p>}
      {!loading && !error && (
        <table style={{ width:"100%",borderCollapse:"collapse",fontSize:14 }}>
          <thead><tr style={{ borderBottom:"2px solid #e5e7eb",textAlign:"left" }}>
            {["Name","Type","Managed","Description","Actions"].map(h=><th key={h} style={{ padding:"8px 12px",fontWeight:600,color:"#374151" }}>{h}</th>)}
          </tr></thead>
          <tbody>
            {networks.length===0 && <tr><td colSpan={5} style={{ padding:24,textAlign:"center",color:"#9ca3af" }}>No networks found</td></tr>}
            {networks.map(n=>(
              <tr key={n.name} style={{ borderBottom:"1px solid #f3f4f6" }}>
                <td style={{ padding:"10px 12px",fontWeight:500 }}>{n.name}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280" }}>{n.type}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280" }}>{n.managed?"Yes":"No"}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280",fontSize:13 }}>{n.description||"—"}</td>
                <td style={{ padding:"10px 12px" }}>
                  {n.managed && <button onClick={()=>setConfirm(n)} style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"none",background:"#ef4444",color:"#fff",cursor:"pointer" }}>Delete</button>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {showCreate && <CreateNetworkDialog onClose={()=>setShowCreate(false)} onCreated={reload} />}
      <ConfirmDialog open={confirm!==null} title="Delete network" message={`Delete "${confirm?.name}"?`} confirmLabel="Delete"
        onConfirm={async()=>{ if(confirm){await api.deleteNetwork(confirm.name);reload();setConfirm(null);} }}
        onCancel={()=>setConfirm(null)} />
    </div>
  );
};
