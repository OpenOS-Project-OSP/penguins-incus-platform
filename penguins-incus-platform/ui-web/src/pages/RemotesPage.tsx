import React, { useState } from "react";
import { api, Remote } from "../api/client";
import { useApi } from "../hooks/useApi";
import { PageHeader } from "../components/PageHeader";
import { ConfirmDialog } from "../components/ConfirmDialog";

export const RemotesPage: React.FC = () => {
  const { data, loading, error, reload } = useApi(() => api.listRemotes(), []);
  const [showAdd, setShowAdd] = useState(false);
  const [rName, setRName] = useState(""); const [rUrl, setRUrl] = useState("https://");
  const [addError, setAddError] = useState(""); const [busy, setBusy] = useState(false);
  const [confirm, setConfirm] = useState<Remote | null>(null);
  const [activating, setActivating] = useState<string | null>(null);
  const remotes: Remote[] = data ?? [];

  const add = async () => {
    if (!rName.trim() || !rUrl.trim()) { setAddError("Name and URL are required"); return; }
    setBusy(true);
    try { await api.addRemote({ name: rName, url: rUrl }); reload(); setShowAdd(false); setRName(""); setRUrl("https://"); }
    catch (e) { setAddError((e as Error).message); } finally { setBusy(false); }
  };

  const activate = async (name: string) => {
    setActivating(name);
    try { await api.activateRemote(name); reload(); }
    catch { /* ignore */ } finally { setActivating(null); }
  };

  return (
    <div style={{ padding:24 }}>
      <PageHeader title="Remotes" onRefresh={reload}
        action={<button onClick={()=>setShowAdd(true)} style={{ padding:"6px 16px",borderRadius:4,border:"none",background:"#1a73e8",color:"#fff",cursor:"pointer" }}>+ Add</button>} />
      {showAdd && (
        <div style={{ background:"#f9fafb",border:"1px solid #e5e7eb",borderRadius:8,padding:16,marginBottom:20 }}>
          <div style={{ display:"flex",gap:12,alignItems:"flex-end",flexWrap:"wrap" }}>
            <label style={{ flex:1,minWidth:140 }}>
              <span style={{ fontSize:13,color:"#555" }}>Name</span>
              <input value={rName} onChange={e=>setRName(e.target.value)} style={{ display:"block",width:"100%",marginTop:4,padding:"6px 8px",border:"1px solid #ddd",borderRadius:4,boxSizing:"border-box" }} />
            </label>
            <label style={{ flex:3,minWidth:240 }}>
              <span style={{ fontSize:13,color:"#555" }}>URL</span>
              <input value={rUrl} onChange={e=>setRUrl(e.target.value)} style={{ display:"block",width:"100%",marginTop:4,padding:"6px 8px",border:"1px solid #ddd",borderRadius:4,boxSizing:"border-box" }} />
            </label>
            <button onClick={add} disabled={busy} style={{ padding:"7px 16px",borderRadius:4,border:"none",background:"#1a73e8",color:"#fff",cursor:"pointer" }}>{busy?"Adding…":"Add"}</button>
            <button onClick={()=>setShowAdd(false)} style={{ padding:"7px 16px",borderRadius:4,border:"1px solid #ddd",cursor:"pointer" }}>Cancel</button>
          </div>
          {addError && <p style={{ color:"#ef4444",margin:"8px 0 0",fontSize:13 }}>{addError}</p>}
        </div>
      )}
      {loading && <p style={{ color:"#888" }}>Loading…</p>}
      {error   && <p style={{ color:"#ef4444" }}>Error: {error}</p>}
      {!loading && !error && (
        <table style={{ width:"100%",borderCollapse:"collapse",fontSize:14 }}>
          <thead><tr style={{ borderBottom:"2px solid #e5e7eb",textAlign:"left" }}>
            {["Name","URL","Protocol","Actions"].map(h=><th key={h} style={{ padding:"8px 12px",fontWeight:600,color:"#374151" }}>{h}</th>)}
          </tr></thead>
          <tbody>
            {remotes.length===0 && <tr><td colSpan={4} style={{ padding:24,textAlign:"center",color:"#9ca3af" }}>No remotes configured</td></tr>}
            {remotes.map(r=>(
              <tr key={r.name} style={{ borderBottom:"1px solid #f3f4f6" }}>
                <td style={{ padding:"10px 12px",fontWeight:500 }}>{r.name}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280",fontSize:12,fontFamily:"monospace" }}>{r.url}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280" }}>{r.protocol||"incus"}</td>
                <td style={{ padding:"10px 12px" }}>
                  <div style={{ display:"flex",gap:4 }}>
                    <button onClick={()=>activate(r.name)} disabled={activating===r.name}
                      style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"1px solid #ddd",cursor:"pointer" }}>
                      {activating===r.name?"Switching…":"Activate"}
                    </button>
                    {r.name!=="local" && <button onClick={()=>setConfirm(r)} style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"none",background:"#ef4444",color:"#fff",cursor:"pointer" }}>Remove</button>}
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <ConfirmDialog open={confirm!==null} title="Remove remote" message={`Remove remote "${confirm?.name}"?`} confirmLabel="Remove"
        onConfirm={async()=>{ if(confirm){await api.removeRemote(confirm.name);reload();setConfirm(null);} }}
        onCancel={()=>setConfirm(null)} />
    </div>
  );
};
