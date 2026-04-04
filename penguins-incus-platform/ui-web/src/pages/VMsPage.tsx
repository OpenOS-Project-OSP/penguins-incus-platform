import React, { useCallback, useState } from "react";
import { api, Instance } from "../api/client";
import { useApi } from "../hooks/useApi";
import { useEvents } from "../hooks/useEvents";
import { StatusBadge } from "../components/StatusBadge";
import { ConfirmDialog } from "../components/ConfirmDialog";
import { PageHeader } from "../components/PageHeader";

const CreateVMDialog: React.FC<{ onClose: () => void; onCreated: () => void }> = ({
  onClose, onCreated,
}) => {
  const [name, setName]   = useState("");
  const [image, setImage] = useState("images:ubuntu/24.04");
  const [error, setError] = useState("");
  const [busy, setBusy]   = useState(false);

  const submit = async () => {
    if (!name.trim()) { setError("Name is required"); return; }
    setBusy(true);
    try {
      await api.createInstance({ name, image, type: "virtual-machine" });
      onCreated(); onClose();
    } catch (e) { setError((e as Error).message); }
    finally { setBusy(false); }
  };

  return (
    <div style={{ position:"fixed", inset:0, background:"rgba(0,0,0,.4)",
                  display:"flex", alignItems:"center", justifyContent:"center", zIndex:1000 }}>
      <div style={{ background:"#fff", borderRadius:8, padding:24, minWidth:360,
                    boxShadow:"0 8px 32px rgba(0,0,0,.2)" }}>
        <h3 style={{ margin:"0 0 16px" }}>Create Virtual Machine</h3>
        <label style={{ display:"block", marginBottom:12 }}>
          <span style={{ fontSize:13, color:"#555" }}>Name</span>
          <input value={name} onChange={e => setName(e.target.value)}
            style={{ display:"block", width:"100%", marginTop:4, padding:"6px 8px",
                     border:"1px solid #ddd", borderRadius:4, boxSizing:"border-box" }} />
        </label>
        <label style={{ display:"block", marginBottom:16 }}>
          <span style={{ fontSize:13, color:"#555" }}>Image</span>
          <input value={image} onChange={e => setImage(e.target.value)}
            style={{ display:"block", width:"100%", marginTop:4, padding:"6px 8px",
                     border:"1px solid #ddd", borderRadius:4, boxSizing:"border-box" }} />
        </label>
        {error && <p style={{ color:"#ef4444", margin:"0 0 12px", fontSize:13 }}>{error}</p>}
        <div style={{ display:"flex", gap:8, justifyContent:"flex-end" }}>
          <button onClick={onClose} disabled={busy}
            style={{ padding:"6px 16px", borderRadius:4, border:"1px solid #ddd", cursor:"pointer" }}>
            Cancel
          </button>
          <button onClick={submit} disabled={busy}
            style={{ padding:"6px 16px", borderRadius:4, border:"none",
                     background:"#1a73e8", color:"#fff", cursor:"pointer" }}>
            {busy ? "Creating…" : "Create"}
          </button>
        </div>
      </div>
    </div>
  );
};

export const VMsPage: React.FC = () => {
  const { data, loading, error, reload } = useApi(
    () => api.listInstances("", "", "virtual-machine"), []
  );
  const [showCreate, setShowCreate]   = useState(false);
  const [confirm, setConfirm]         = useState<{ name: string; project: string } | null>(null);
  const [busy, setBusy]               = useState<Record<string, boolean>>({});
  const [actionError, setActionError] = useState<string | null>(null);

  useEvents(useCallback((e) => { if (e.type === "lifecycle") reload(); }, [reload]));

  const withBusy = async (name: string, fn: () => Promise<unknown>) => {
    setBusy(b => ({ ...b, [name]: true }));
    setActionError(null);
    try { await fn(); reload(); }
    catch (e) { setActionError((e as Error).message); }
    finally { setBusy(b => ({ ...b, [name]: false })); }
  };

  const vms: Instance[] = data ?? [];

  return (
    <div style={{ padding: 24 }}>
      <PageHeader title="Virtual Machines" onRefresh={reload}
        action={
          <button onClick={() => setShowCreate(true)}
            style={{ padding:"6px 16px", borderRadius:4, border:"none",
                     background:"#1a73e8", color:"#fff", cursor:"pointer" }}>
            + Create
          </button>
        }
      />
      {actionError && (
        <div style={{ background:"#fef2f2", border:"1px solid #fca5a5", borderRadius:4,
                      padding:"8px 12px", marginBottom:16, color:"#b91c1c", fontSize:13 }}>
          {actionError}
        </div>
      )}
      {loading && <p style={{ color:"#888" }}>Loading…</p>}
      {error   && <p style={{ color:"#ef4444" }}>Error: {error}</p>}
      {!loading && !error && (
        <table style={{ width:"100%", borderCollapse:"collapse", fontSize:14 }}>
          <thead>
            <tr style={{ borderBottom:"2px solid #e5e7eb", textAlign:"left" }}>
              {["Name","Status","Image","Project","CPU","Memory","Actions"].map(h => (
                <th key={h} style={{ padding:"8px 12px", fontWeight:600, color:"#374151" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {vms.length === 0 && (
              <tr><td colSpan={7} style={{ padding:24, textAlign:"center", color:"#9ca3af" }}>
                No virtual machines found
              </td></tr>
            )}
            {vms.map(vm => (
              <tr key={vm.name} style={{ borderBottom:"1px solid #f3f4f6" }}>
                <td style={{ padding:"10px 12px", fontWeight:500 }}>{vm.name}</td>
                <td style={{ padding:"10px 12px" }}><StatusBadge status={vm.status} /></td>
                <td style={{ padding:"10px 12px", color:"#6b7280", fontSize:13 }}>{vm.image ?? "—"}</td>
                <td style={{ padding:"10px 12px", color:"#6b7280" }}>{vm.project}</td>
                <td style={{ padding:"10px 12px", color:"#6b7280" }}>
                  {vm.cpu_usage != null ? `${(vm.cpu_usage * 100).toFixed(1)}%` : "—"}
                </td>
                <td style={{ padding:"10px 12px", color:"#6b7280" }}>
                  {vm.memory_usage_bytes != null
                    ? `${(vm.memory_usage_bytes / 1024 / 1024).toFixed(0)} MB` : "—"}
                </td>
                <td style={{ padding:"10px 12px" }}>
                  <div style={{ display:"flex", gap:4, flexWrap:"wrap" }}>
                    {vm.status === "Stopped" && (
                      <button disabled={busy[vm.name]} onClick={() => withBusy(vm.name, () =>
                        api.changeInstanceState(vm.name, "start", false, vm.project))}
                        style={{ padding:"3px 10px", fontSize:12, borderRadius:4,
                                 border:"1px solid #ddd", cursor:"pointer" }}>Start</button>
                    )}
                    {vm.status === "Running" && (<>
                      <button disabled={busy[vm.name]} onClick={() => withBusy(vm.name, () =>
                        api.changeInstanceState(vm.name, "stop", false, vm.project))}
                        style={{ padding:"3px 10px", fontSize:12, borderRadius:4,
                                 border:"1px solid #ddd", cursor:"pointer" }}>Stop</button>
                      <button disabled={busy[vm.name]} onClick={() => withBusy(vm.name, () =>
                        api.changeInstanceState(vm.name, "restart", false, vm.project))}
                        style={{ padding:"3px 10px", fontSize:12, borderRadius:4,
                                 border:"1px solid #ddd", cursor:"pointer" }}>Restart</button>
                      <a href={api.consoleWsUrl(vm.name, vm.project)}
                        target="_blank" rel="noreferrer"
                        style={{ padding:"3px 10px", fontSize:12, borderRadius:4,
                                 border:"1px solid #ddd", textDecoration:"none",
                                 color:"inherit", display:"inline-block" }}>Console</a>
                    </>)}
                    <button onClick={() => setConfirm({ name: vm.name, project: vm.project })}
                      style={{ padding:"3px 10px", fontSize:12, borderRadius:4,
                               border:"none", background:"#ef4444", color:"#fff", cursor:"pointer" }}>
                      Delete
                    </button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
      {showCreate && <CreateVMDialog onClose={() => setShowCreate(false)} onCreated={reload} />}
      <ConfirmDialog
        open={confirm !== null}
        title="Delete virtual machine"
        message={`Delete "${confirm?.name}"? This cannot be undone.`}
        confirmLabel="Delete"
        onConfirm={() => {
          if (!confirm) return;
          withBusy(confirm.name, () => api.deleteInstance(confirm.name, confirm.project, true));
          setConfirm(null);
        }}
        onCancel={() => setConfirm(null)}
      />
    </div>
  );
};
