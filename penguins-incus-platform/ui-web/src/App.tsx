import { Routes, Route, NavLink } from "react-router-dom";
import { ContainersPage }  from "./pages/ContainersPage";
import { VMsPage }         from "./pages/VMsPage";
import { NetworksPage }    from "./pages/NetworksPage";
import { StoragePage }     from "./pages/StoragePage";
import { ImagesPage }      from "./pages/ImagesPage";
import { ProfilesPage }    from "./pages/ProfilesPage";
import { ProjectsPage }    from "./pages/ProjectsPage";
import { ClusterPage }     from "./pages/ClusterPage";
import { RemotesPage }     from "./pages/RemotesPage";
import { OperationsPage }  from "./pages/OperationsPage";
import { EventsPage }      from "./pages/EventsPage";

const NAV = [
  { path: "/",           label: "Containers",  element: <ContainersPage /> },
  { path: "/vms",        label: "VMs",         element: <VMsPage /> },
  { path: "/networks",   label: "Networks",    element: <NetworksPage /> },
  { path: "/storage",    label: "Storage",     element: <StoragePage /> },
  { path: "/images",     label: "Images",      element: <ImagesPage /> },
  { path: "/profiles",   label: "Profiles",    element: <ProfilesPage /> },
  { path: "/projects",   label: "Projects",    element: <ProjectsPage /> },
  { path: "/cluster",    label: "Cluster",     element: <ClusterPage /> },
  { path: "/remotes",    label: "Remotes",     element: <RemotesPage /> },
  { path: "/operations", label: "Operations",  element: <OperationsPage /> },
  { path: "/events",     label: "Events",      element: <EventsPage /> },
];

export default function App() {
  return (
    <div style={{ display:"flex", height:"100vh", fontFamily:"system-ui,sans-serif" }}>
      <nav style={{ width:200, borderRight:"1px solid #e5e7eb", padding:"12px 8px",
                    display:"flex", flexDirection:"column", gap:2, background:"#fafafa" }}>
        <div style={{ fontWeight:700, fontSize:14, padding:"8px 8px 16px",
                      color:"#111", borderBottom:"1px solid #e5e7eb", marginBottom:8 }}>
          Kapsule Incus Manager
        </div>
        {NAV.map(({ path, label }) => (
          <NavLink key={path} to={path} end={path === "/"}
            style={({ isActive }) => ({
              display:"block", padding:"7px 10px", borderRadius:6,
              textDecoration:"none", fontSize:14,
              background: isActive ? "#e8f0fe" : "transparent",
              color: isActive ? "#1a73e8" : "#374151",
              fontWeight: isActive ? 600 : 400,
            })}>
            {label}
          </NavLink>
        ))}
      </nav>
      <main style={{ flex:1, overflow:"auto" }}>
        <Routes>
          {NAV.map(({ path, element }) => (
            <Route key={path} path={path} element={element} />
          ))}
        </Routes>
      </main>
    </div>
  );
}
