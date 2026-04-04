/**
 * PIP daemon REST API client.
 * All methods map 1:1 to endpoints in api/schema/openapi.yaml.
 */

const BASE = "/api/v1";

async function request<T>(
  method: string,
  path: string,
  body?: unknown,
  params?: Record<string, string>
): Promise<T> {
  const url = new URL(BASE + path, window.location.origin);
  if (params) {
    Object.entries(params).forEach(([k, v]) => v && url.searchParams.set(k, v));
  }
  const res = await fetch(url.toString(), {
    method,
    headers: body ? { "Content-Type": "application/json" } : {},
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ message: res.statusText }));
    throw new Error(err.message ?? res.statusText);
  }
  if (res.status === 204) return undefined as T;
  return res.json() as Promise<T>;
}

const get  = <T>(path: string, params?: Record<string, string>) => request<T>("GET",    path, undefined, params);
const post = <T>(path: string, body?: unknown)                   => request<T>("POST",   path, body);
const put  = <T>(path: string, body?: unknown)                   => request<T>("PUT",    path, body);
const del  = <T>(path: string, params?: Record<string, string>) => request<T>("DELETE", path, undefined, params);

// ── Types ─────────────────────────────────────────────────────────────────────

export type InstanceStatus = "Running" | "Stopped" | "Frozen" | "Error" | "Unknown";
export type InstanceType   = "container" | "virtual-machine";

export interface Instance {
  name: string;
  type: InstanceType;
  status: InstanceStatus;
  image?: string;
  project: string;
  remote: string;
  created_at?: string;
  cpu_usage?: number;
  memory_usage_bytes?: number;
  disk_usage_bytes?: number;
}

export interface Network {
  name: string;
  type: string;
  description?: string;
  managed: boolean;
  config?: Record<string, string>;
  project?: string;
}

export interface StoragePool {
  name: string;
  driver: string;
  description?: string;
  config?: Record<string, string>;
  status?: string;
}

export interface StorageVolume {
  name: string;
  type: string;
  description?: string;
  config?: Record<string, string>;
  pool?: string;
}

export interface Image {
  fingerprint: string;
  description: string;
  os?: string;
  release?: string;
  architecture?: string;
  size_bytes?: number;
  uploaded_at?: string;
  aliases?: string[];
  remote?: string;
}

export interface Profile {
  name: string;
  description?: string;
  config?: Record<string, string>;
  devices?: Record<string, unknown>;
  project?: string;
}

export interface ProfilePreset {
  name: string;
  description: string;
  category: string;
  profile: Profile;
}

export interface Project {
  name: string;
  description?: string;
  config?: Record<string, string>;
}

export interface ClusterMember {
  name: string;
  url: string;
  status: "Online" | "Offline" | "Evacuated";
  roles?: string[];
  architecture?: string;
  description?: string;
}

export interface Remote {
  name: string;
  url: string;
  protocol?: string;
  auth_type?: string;
  public?: boolean;
}

export interface Operation {
  id: string;
  description: string;
  status: "pending" | "running" | "succeeded" | "failed" | "cancelled";
  created_at: string;
  updated_at?: string;
  metadata?: Record<string, unknown>;
  error?: string;
}

export interface KimEvent {
  type: string;
  timestamp: string;
  project?: string;
  location?: string;
  metadata: Record<string, unknown>;
}

// ── API methods ───────────────────────────────────────────────────────────────

export const api = {
  // Instances
  listInstances:       (project = "", remote = "", type = "") =>
    get<Instance[]>("/instances", { project, remote, type }),
  createInstance:      (config: Partial<Instance> & { image: string }) =>
    post<Operation>("/instances", config),
  getInstance:         (name: string, project = "") =>
    get<Instance>(`/instances/${name}`, { project }),
  deleteInstance:      (name: string, project = "", force = false) =>
    del<Operation>(`/instances/${name}`, { project, force: String(force) }),
  changeInstanceState: (name: string, action: string, force = false, project = "") =>
    put<Operation>(`/instances/${name}/state`, { action, force, project }),
  renameInstance:      (name: string, newName: string, project = "") =>
    post<Operation>(`/instances/${name}/rename`, { new_name: newName, project }),
  listSnapshots:       (name: string, project = "") =>
    get<{ name: string; created_at: string; stateful: boolean }[]>(
      `/instances/${name}/snapshots`, { project }),
  createSnapshot:      (name: string, snapshot: string, stateful = false, project = "") =>
    post<Operation>(`/instances/${name}/snapshots`, { name: snapshot, stateful, project }),
  restoreSnapshot:     (name: string, snapshot: string, project = "") =>
    post<Operation>(`/instances/${name}/snapshots/${snapshot}`, { project }),
  deleteSnapshot:      (name: string, snapshot: string, project = "") =>
    del<Operation>(`/instances/${name}/snapshots/${snapshot}`, { project }),
  getInstanceLogs:     (name: string, project = "") =>
    get<string>(`/instances/${name}/logs`, { project }),
  execWsUrl:           (name: string, project = "", command = "/bin/bash") =>
    `/api/v1/instances/${name}/exec/ws?command=${encodeURIComponent(command)}&project=${project}`,
  consoleWsUrl:        (name: string, project = "") =>
    `/api/v1/instances/${name}/console/ws?project=${project}`,

  // Networks
  listNetworks:   (project = "") => get<Network[]>("/networks", { project }),
  createNetwork:  (config: Partial<Network>) => post<Operation>("/networks", config),
  getNetwork:     (name: string, project = "") => get<Network>(`/networks/${name}`, { project }),
  updateNetwork:  (name: string, config: Partial<Network>, project = "") =>
    put<void>(`/networks/${name}`, { ...config, project }),
  deleteNetwork:  (name: string, project = "") =>
    del<Operation>(`/networks/${name}`, { project }),

  // Storage
  listStoragePools:   () => get<StoragePool[]>("/storage-pools"),
  createStoragePool:  (config: Partial<StoragePool>) => post<Operation>("/storage-pools", config),
  getStoragePool:     (name: string) => get<StoragePool>(`/storage-pools/${name}`),
  deleteStoragePool:  (name: string) => del<Operation>(`/storage-pools/${name}`),
  listVolumes:        (pool: string, project = "") =>
    get<StorageVolume[]>(`/storage-pools/${pool}/volumes`, { project }),
  createVolume:       (pool: string, config: Partial<StorageVolume>) =>
    post<Operation>(`/storage-pools/${pool}/volumes`, config),
  deleteVolume:       (pool: string, name: string, project = "") =>
    del<Operation>(`/storage-pools/${pool}/volumes/${name}`, { project }),

  // Images
  listImages:   (remote = "") => get<Image[]>("/images", { remote }),
  pullImage:    (remote: string, image: string, alias = "") =>
    post<Operation>("/images", { remote, image, alias }),
  getImage:     (fingerprint: string) => get<Image>(`/images/${fingerprint}`),
  deleteImage:  (fingerprint: string) => del<Operation>(`/images/${fingerprint}`),

  // Profiles
  listProfiles:   (project = "") => get<Profile[]>("/profiles", { project }),
  createProfile:  (config: Partial<Profile>) => post<Operation>("/profiles", config),
  getProfile:     (name: string, project = "") => get<Profile>(`/profiles/${name}`, { project }),
  updateProfile:  (name: string, config: Partial<Profile>, project = "") =>
    put<void>(`/profiles/${name}`, { ...config, project }),
  deleteProfile:  (name: string, project = "") =>
    del<Operation>(`/profiles/${name}`, { project }),
  listPresets:    () => get<ProfilePreset[]>("/profiles/presets"),

  // Projects
  listProjects:   () => get<Project[]>("/projects"),
  createProject:  (config: Partial<Project>) => post<Operation>("/projects", config),
  getProject:     (name: string) => get<Project>(`/projects/${name}`),
  updateProject:  (name: string, config: Partial<Project>) =>
    put<void>(`/projects/${name}`, config),
  deleteProject:  (name: string) => del<Operation>(`/projects/${name}`),

  // Cluster
  listClusterMembers:    () => get<ClusterMember[]>("/cluster/members"),
  getClusterMember:      (name: string) => get<ClusterMember>(`/cluster/members/${name}`),
  removeClusterMember:   (name: string) => del<Operation>(`/cluster/members/${name}`),
  evacuateClusterMember: (name: string) =>
    post<Operation>(`/cluster/members/${name}/evacuate`),
  restoreClusterMember:  (name: string) =>
    post<Operation>(`/cluster/members/${name}/restore`),

  // Remotes
  listRemotes:    () => get<Remote[]>("/remotes"),
  addRemote:      (config: Partial<Remote>) => post<Remote>("/remotes", config),
  getRemote:      (name: string) => get<Remote>(`/remotes/${name}`),
  removeRemote:   (name: string) => del<void>(`/remotes/${name}`),
  activateRemote: (name: string) => put<{ active: string }>(`/remotes/${name}/activate`),

  // Operations
  listOperations:  (status = "") => get<Operation[]>("/operations", { status }),
  getOperation:    (id: string) => get<Operation>(`/operations/${id}`),
  cancelOperation: (id: string) => del<Operation>(`/operations/${id}`),

  // Events (SSE)
  eventSource: (type = "", project = "") => {
    const url = new URL("/api/v1/events", window.location.origin);
    if (type)    url.searchParams.set("type", type);
    if (project) url.searchParams.set("project", project);
    return new EventSource(url.toString());
  },

  // Provisioning
  deployCompose:  (config: Record<string, unknown>) =>
    post<Operation>("/provisioning/compose", config),
  convertCompose: (compose: string) =>
    post<Record<string, unknown>>("/provisioning/compose/convert", { compose }),
};
