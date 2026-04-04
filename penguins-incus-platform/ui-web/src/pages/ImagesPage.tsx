import React, { useState } from "react";
import { api, Image } from "../api/client";
import { useApi } from "../hooks/useApi";
import { PageHeader } from "../components/PageHeader";
import { ConfirmDialog } from "../components/ConfirmDialog";

const PullImageDialog: React.FC<{ onClose: () => void; onPulled: () => void }> = ({ onClose, onPulled }) => {
  const [remote, setRemote] = useState("images"); const [image, setImage] = useState("ubuntu/24.04");
  const [alias, setAlias] = useState(""); const [error, setError] = useState(""); const [busy, setBusy] = useState(false);
  const submit = async () => {
    setBusy(true);
    try { await api.pullImage(remote, image, alias); onPulled(); onClose(); }
    catch (e) { setError((e as Error).message); } finally { setBusy(false); }
  };
  return (
    <div style={{ position:"fixed",inset:0,background:"rgba(0,0,0,.4)",display:"flex",alignItems:"center",justifyContent:"center",zIndex:1000 }}>
      <div style={{ background:"#fff",borderRadius:8,padding:24,minWidth:380,boxShadow:"0 8px 32px rgba(0,0,0,.2)" }}>
        <h3 style={{ margin:"0 0 16px" }}>Pull Image</h3>
        {[["Remote","text",remote,setRemote],["Image","text",image,setImage],["Alias (optional)","text",alias,setAlias]].map(([label,,val,set])=>(
          <label key={label as string} style={{ display:"block",marginBottom:12 }}>
            <span style={{ fontSize:13,color:"#555" }}>{label as string}</span>
            <input value={val as string} onChange={e=>(set as (v:string)=>void)(e.target.value)}
              style={{ display:"block",width:"100%",marginTop:4,padding:"6px 8px",border:"1px solid #ddd",borderRadius:4,boxSizing:"border-box" }} />
          </label>
        ))}
        {error && <p style={{ color:"#ef4444",margin:"0 0 12px",fontSize:13 }}>{error}</p>}
        <div style={{ display:"flex",gap:8,justifyContent:"flex-end" }}>
          <button onClick={onClose} disabled={busy} style={{ padding:"6px 16px",borderRadius:4,border:"1px solid #ddd",cursor:"pointer" }}>Cancel</button>
          <button onClick={submit} disabled={busy} style={{ padding:"6px 16px",borderRadius:4,border:"none",background:"#1a73e8",color:"#fff",cursor:"pointer" }}>{busy?"Pulling…":"Pull"}</button>
        </div>
      </div>
    </div>
  );
};

const fmt = (bytes?: number) => bytes ? `${(bytes/1024/1024).toFixed(0)} MB` : "—";

export const ImagesPage: React.FC = () => {
  const { data, loading, error, reload } = useApi(() => api.listImages(), []);
  const [showPull, setShowPull] = useState(false);
  const [confirm, setConfirm] = useState<Image | null>(null);
  const images: Image[] = data ?? [];
  return (
    <div style={{ padding:24 }}>
      <PageHeader title="Images" onRefresh={reload}
        action={<button onClick={()=>setShowPull(true)} style={{ padding:"6px 16px",borderRadius:4,border:"none",background:"#1a73e8",color:"#fff",cursor:"pointer" }}>↓ Pull</button>} />
      {loading && <p style={{ color:"#888" }}>Loading…</p>}
      {error   && <p style={{ color:"#ef4444" }}>Error: {error}</p>}
      {!loading && !error && (
        <table style={{ width:"100%",borderCollapse:"collapse",fontSize:14 }}>
          <thead><tr style={{ borderBottom:"2px solid #e5e7eb",textAlign:"left" }}>
            {["Fingerprint","Description","OS","Release","Arch","Size","Actions"].map(h=><th key={h} style={{ padding:"8px 12px",fontWeight:600,color:"#374151" }}>{h}</th>)}
          </tr></thead>
          <tbody>
            {images.length===0 && <tr><td colSpan={7} style={{ padding:24,textAlign:"center",color:"#9ca3af" }}>No images found</td></tr>}
            {images.map(img=>(
              <tr key={img.fingerprint} style={{ borderBottom:"1px solid #f3f4f6" }}>
                <td style={{ padding:"10px 12px",fontFamily:"monospace",fontSize:12 }}>{img.fingerprint.slice(0,12)}…</td>
                <td style={{ padding:"10px 12px" }}>{img.description}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280" }}>{img.os||"—"}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280" }}>{img.release||"—"}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280" }}>{img.architecture||"—"}</td>
                <td style={{ padding:"10px 12px",color:"#6b7280" }}>{fmt(img.size_bytes)}</td>
                <td style={{ padding:"10px 12px" }}>
                  <button onClick={()=>setConfirm(img)} style={{ padding:"3px 10px",fontSize:12,borderRadius:4,border:"none",background:"#ef4444",color:"#fff",cursor:"pointer" }}>Delete</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {showPull && <PullImageDialog onClose={()=>setShowPull(false)} onPulled={reload} />}
      <ConfirmDialog open={confirm!==null} title="Delete image" message={`Delete image ${confirm?.fingerprint.slice(0,12)}…?`} confirmLabel="Delete"
        onConfirm={async()=>{ if(confirm){await api.deleteImage(confirm.fingerprint);reload();setConfirm(null);} }}
        onCancel={()=>setConfirm(null)} />
    </div>
  );
};
