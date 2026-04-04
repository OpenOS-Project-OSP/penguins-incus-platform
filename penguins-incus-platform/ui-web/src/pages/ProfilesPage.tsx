import React, { useState } from "react";
import { api, Profile, ProfilePreset } from "../api/client";
import { useApi } from "../hooks/useApi";
import { PageHeader } from "../components/PageHeader";
import { ConfirmDialog } from "../components/ConfirmDialog";

export const ProfilesPage: React.FC = () => {
  const { data, loading, error, reload } = useApi(() => api.listProfiles(), []);
  const { data: presets } = useApi(() => api.listPresets(), []);
  const [confirm, setConfirm] = useState<Profile | null>(null);
  const [applyBusy, setApplyBusy] = useState<string | null>(null);
  const profiles: Profile[] = data ?? [];
  const presetList: ProfilePreset[] = presets ?? [];

  const applyPreset = async (preset: ProfilePreset) => {
    setApplyBusy(preset.name);
    try { await api.createProfile(preset.profile); reload(); }
    catch { /* already exists — ignore */ }
    finally { setApplyBusy(null); }
  };

  return (
    <div style={{ padding:24 }}>
      <PageHeader title="Profiles" onRefresh={reload} />

      {presetList.length > 0 && (
        <div style={{ marginBottom:24 }}>
          <h3 style={{ margin:"0 0 12px",fontSize:15,fontWeight:600 }}>Preset Library</h3>
          <div style={{ display:"flex",gap:8,flexWrap:"wrap" }}>
            {presetList.map(p=>(
              <button key={p.name} onClick={()=>applyPreset(p)} disabled={applyBusy===p.name}
                style={{ padding:"6px 14px",borderRadius:4,border:"1px solid #ddd",cursor:"pointer",
                         background:"#f9fafb",fontSize:13 }}>
                {applyBusy===p.name?"Applying…":`+ ${p.name}`}
                <span style={{ marginLeft:6,fontSize:11,color:"#9ca3af" }}>{p.category}</span>
              </button>
            ))}
          </div>
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
            {profiles.length===0 && <tr><td colSpan={3} style={{ padding:24,textAlign:"center",color:"#9ca3af" }}>No profiles found</td></tr>}
            {profiles.map(p=>(
              <tr key={p.name} style={{ borderBottom:"1px solid #f3f4f6" }}>
                <td style={{ padding:"10px 12px",fontWeight:500 }}>{p.name}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280",fontSize:13 }}>{p.description||"—"}</td>
                <td style={{ padding:"10px 12px" }}>
                  {p.name!=="default" && (
                    <button onClick={()=>setConfirm(p)} style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"none",background:"#ef4444",color:"#fff",cursor:"pointer" }}>Delete</button>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      <ConfirmDialog open={confirm!==null} title="Delete profile" message={`Delete "${confirm?.name}"?`} confirmLabel="Delete"
        onConfirm={async()=>{ if(confirm){await api.deleteProfile(confirm.name);reload();setConfirm(null);} }}
        onCancel={()=>setConfirm(null)} />
    </div>
  );
};
