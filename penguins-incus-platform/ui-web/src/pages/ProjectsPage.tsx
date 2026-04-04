import React, { useState } from "react";
import { api, Project } from "../api/client";
import { useApi } from "../hooks/useApi";
import { PageHeader } from "../components/PageHeader";
import { ConfirmDialog } from "../components/ConfirmDialog";

export const ProjectsPage: React.FC = () => {
  const { data, loading, error, reload } = useApi(() => api.listProjects(), []);
  const [showCreate, setShowCreate] = useState(false);
  const [name, setName] = useState(""); const [desc, setDesc] = useState("");
  const [createError, setCreateError] = useState(""); const [busy, setBusy] = useState(false);
  const [confirm, setConfirm] = useState<Project | null>(null);
  const projects: Project[] = data ?? [];

  const create = async () => {
    if (!name.trim()) { setCreateError("Name is required"); return; }
    setBusy(true);
    try { await api.createProject({ name, description: desc }); reload(); setShowCreate(false); setName(""); setDesc(""); }
    catch (e) { setCreateError((e as Error).message); } finally { setBusy(false); }
  };

  return (
    <div style={{ padding:24 }}>
      <PageHeader title="Projects" onRefresh={reload}
        action={<button onClick={()=>setShowCreate(true)} style={{ padding:"6px 16px",borderRadius:4,border:"none",background:"#1a73e8",color:"#fff",cursor:"pointer" }}>+ Create</button>} />
      {showCreate && (
        <div style={{ background:"#f9fafb",border:"1px solid #e5e7eb",borderRadius:8,padding:16,marginBottom:20 }}>
          <div style={{ display:"flex",gap:12,alignItems:"flex-end",flexWrap:"wrap" }}>
            <label style={{ flex:1,minWidth:160 }}>
              <span style={{ fontSize:13,color:"#555" }}>Name</span>
              <input value={name} onChange={e=>setName(e.target.value)} style={{ display:"block",width:"100%",marginTop:4,padding:"6px 8px",border:"1px solid #ddd",borderRadius:4,boxSizing:"border-box" }} />
            </label>
            <label style={{ flex:2,minWidth:200 }}>
              <span style={{ fontSize:13,color:"#555" }}>Description</span>
              <input value={desc} onChange={e=>setDesc(e.target.value)} style={{ display:"block",width:"100%",marginTop:4,padding:"6px 8px",border:"1px solid #ddd",borderRadius:4,boxSizing:"border-box" }} />
            </label>
            <button onClick={create} disabled={busy} style={{ padding:"7px 16px",borderRadius:4,border:"none",background:"#1a73e8",color:"#fff",cursor:"pointer" }}>{busy?"Creating…":"Create"}</button>
            <button onClick={()=>setShowCreate(false)} style={{ padding:"7px 16px",borderRadius:4,border:"1px solid #ddd",cursor:"pointer" }}>Cancel</button>
          </div>
          {createError && <p style={{ color:"#ef4444",margin:"8px 0 0",fontSize:13 }}>{createError}</p>}
        </div>
      )}
      {loading && <p style={{ color:"#888" }}>Loading…</p>}
      {error   && <p style={{ color:"#ef4444" }}>Error: {error}</p>}
      {!loading && !error && (
        <table style={{ width:"100%",borderCollapse:"collapse",fontSize:14 }}>
          <thead><tr style={{ borderBottom:"2px solid #e5e7eb",textAlign:"left" }}>
            {["Name","Description","Actions"].map(h=><th key={h} style={{ padding:"8px 12px",fontWeight:600,color:"#374151" }}>{h}</th>)}
          </tr></thead>
          <tbody>
            {projects.length===0 && <tr><td colSpan={3} style={{ padding:24,textAlign:"center",color:"#9ca3af" }}>No projects found</td></tr>}
            {projects.map(p=>(
              <tr key={p.name} style={{ borderBottom:"1px solid #f3f4f6" }}>
                <td style={{ padding:"10px 12px",fontWeight:500 }}>{p.name}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280",fontSize:13 }}>{p.description||"—"}</td>
                <td style={{ padding:"10px 12px" }}>
                  {p.name!=="default" && <button onClick={()=>setConfirm(p)} style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"none",background:"#ef4444",color:"#fff",cursor:"pointer" }}>Delete</button>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <ConfirmDialog open={confirm!==null} title="Delete project" message={`Delete "${confirm?.name}"?`} confirmLabel="Delete"
        onConfirm={async()=>{ if(confirm){await api.deleteProject(confirm.name);reload();setConfirm(null);} }}
        onCancel={()=>setConfirm(null)} />
    </div>
  );
};
