# Penguins-Incus-Platform — Architecture

## Overview

Penguins-Incus-Platform is a unified Incus container and VM management platform
consisting of three first-class frontends (QML desktop UI, web UI, CLI) backed
by a single daemon. All frontends have full feature parity — every operation
available in one is available in all others.

PIP is also the central control plane for four guest-type toolkits that were
previously maintained as separate projects. Their provisioning logic now runs
inside `penguins-incus-daemon` as plugins, exposed through the same REST/D-Bus API used
by the GUI frontends:

| Source project | Guest type | Daemon plugin | CLI entry point |
|---|---|---|---|
| incusbox | Generic Linux containers | `provisioning/generic.py` | `penguins-incus provision generic` |
| waydroid-toolkit | Waydroid (Android) containers | `provisioning/waydroid.py` | `penguins-incus provision waydroid` |
| Incus-MacOS-Toolkit | macOS KVM VMs | `provisioning/macos.py` | `penguins-incus provision macos` |
| incus-windows-toolkit | Windows VMs | `provisioning/windows.py` | `penguins-incus provision windows` |

## Design Principles

1. **Daemon is the control plane.** No frontend contains business logic,
   validation, or direct Incus API calls. The daemon is the only process that
   talks to `incusd`.

2. **Schema-first API.** The daemon API is defined in `api/schema/openapi.yaml`
   before any implementation. CLI subcommands and D-Bus interfaces are derived
   from this schema. Parity is structural, not maintained by discipline.

3. **Dual transport, one implementation.** The daemon exposes every capability
   over both HTTP REST (for the web UI and remote access) and D-Bus (for the
   QML UI and CLI on the local machine). Both transports call the same internal
   handler functions.

4. **Frontends are thin clients.** QML, web, and CLI contain only presentation
   and transport logic. No frontend duplicates state management or validation.

5. **Feature parity is a hard constraint.** A feature does not ship until it is
   implemented in the daemon API and all three frontends expose it.

---

## Repository Structure

```
penguins-incus-platform/
│
├── ARCHITECTURE.md               this document
│
├── api/
│   └── schema/
│       ├── openapi.yaml          canonical REST API definition
│       └── dbus/
│           └── org.KapsuleIncusManager.xml   D-Bus introspection
│
├── daemon/                       Python — system daemon
│   ├── pyproject.toml
│   ├── penguins_incus/
│   │   ├── main.py               entry point, service wiring
│   │   ├── incus/                Incus REST API client (multi-remote, exec, file push)
│   │   ├── api/
│   │   │   ├── rest/             FastAPI HTTP + WebSocket + SSE server
│   │   │   │   ├── provisioning_generic.py   incusbox routes
│   │   │   │   ├── provisioning_waydroid.py  waydroid-toolkit routes
│   │   │   │   ├── provisioning_macos.py     Incus-MacOS-Toolkit routes
│   │   │   │   └── provisioning_windows.py   incus-windows-toolkit routes
│   │   │   └── dbus/             D-Bus service (dasbus)
│   │   ├── provisioning/         guest-type provisioning plugins
│   │   │   ├── _base.py          shared helpers (cloud-init, device builders)
│   │   │   ├── compose.py        Docker Compose → Incus converter
│   │   │   ├── generic.py        incusbox feature set
│   │   │   ├── waydroid.py       waydroid-toolkit feature set
│   │   │   ├── macos.py          Incus-MacOS-Toolkit feature set
│   │   │   └── windows.py        incus-windows-toolkit feature set
│   │   ├── profiles/             bundled Incus profile library loader
│   │   └── events.py             Incus event subscriber + fan-out
│   └── data/
│       ├── penguins-incus.service           systemd unit
│       └── penguins-incus.socket            systemd socket activation
│
├── ui-qml/                       C++/QML — primary desktop UI
│   ├── CMakeLists.txt
│   ├── lib/                      libpenguins-incus-qt — D-Bus client library (LGPL-2.1)
│   │   ├── CMakeLists.txt
│   │   └── src/
│   └── app/                      QML application
│       ├── CMakeLists.txt
│       ├── main.cpp
│       └── qml/
│
├── ui-web/                       React/TypeScript — web UI
│   ├── package.json
│   └── src/
│
├── cli/                          Python — CLI (thin client over daemon HTTP)
│   ├── pyproject.toml
│   └── penguins_incus/
│       └── cli/
│           ├── main.py               Click-based CLI, generated from OpenAPI schema
│           ├── provision_generic.py  incusbox CLI subcommands
│           ├── provision_waydroid.py waydroid-toolkit CLI subcommands
│           ├── provision_macos.py    Incus-MacOS-Toolkit CLI subcommands
│           └── provision_windows.py  incus-windows-toolkit CLI subcommands
│
├── profiles/                     Incus profile YAML library
│   ├── gpu/
│   ├── audio/
│   ├── display/
│   ├── rocm/
│   ├── nesting/
│   ├── generic/                  incusbox profiles (base, gui, init, nvidia, rootless, …)
│   ├── macos/                    macOS KVM profile (OVMF, Q35, ignore_msrs)
│   ├── windows/                  Windows VM profiles (desktop, server, GPU overlays)
│   └── waydroid/                 Waydroid container profile (binder, ashmem, ADB proxy)
│
└── .devcontainer/
    └── devcontainer.json
```

---

## Component Responsibilities

### daemon (`penguins-incus`)

The daemon is a Python process managed by systemd. It:

- Maintains a persistent connection to the local Incus REST API socket
  (`/var/lib/incus/unix.socket` or via HTTPS for remote servers)
- Subscribes to the Incus event stream and fans out to all connected clients
  via D-Bus signals and HTTP SSE/WebSocket
- Exposes the full PIP API over:
  - **HTTP REST + WebSocket** on `127.0.0.1:8765` (configurable)
  - **D-Bus** on the session or system bus at `org.KapsuleIncusManager`
- Handles all provisioning logic (app containers, Compose deployment, VLAN
  management, profile application)
- Serves the web UI static assets from the same HTTP server
- Starts on demand via systemd socket activation — no manual start required

**Key dependencies:**
- `fastapi` + `uvicorn` — HTTP server
- `dasbus` — D-Bus service
- `httpx` — async Incus REST client
- `websockets` — PTY proxy for terminal access

### ui-qml

A Qt6/QML application that communicates with the daemon exclusively over D-Bus.
It uses `libpenguins-incus-qt` (LGPL-2.1) as the D-Bus client library, which can also be
used by third-party applications.

The QML UI is the primary desktop experience. It integrates with KDE Plasma
where available (Konsole, system tray, KIO) but runs on any Qt6 desktop.

For terminal access (exec into container), the QML UI connects to the daemon's
WebSocket PTY endpoint — the same endpoint used by the web UI — and renders it
via an embedded terminal widget.

### ui-web

The web UI is the React/TypeScript application from `incus-ui-canonical`,
adapted to talk to the PIP daemon REST API instead of directly to Incus. It is
served as static assets by the daemon's HTTP server.

The web UI is the primary interface for remote/headless server management and
for operations outside the scope of the desktop companion (cluster management,
certificate management, raw profile editing).

### cli

A Python CLI built with Click. Subcommands are generated from the OpenAPI
schema to guarantee parity. The CLI communicates with the daemon over HTTP
REST (localhost by default, configurable for remote daemons).

The CLI auto-starts the daemon via systemd socket activation if it is not
already running.

---

## API Transport Strategy

### Why two transports

D-Bus is the correct IPC mechanism for a native desktop application on Linux:
it is low-latency, type-safe, integrates with systemd and polkit for
authorization, and is the standard for KDE/GNOME integration.

HTTP REST is necessary for the web UI (browser cannot use D-Bus) and for
remote access (managing a server from a different machine).

Both transports are first-class. Neither is a wrapper around the other — both
call the same internal Python handler functions directly.

### Schema-first parity contract

`api/schema/openapi.yaml` is the authoritative definition of every operation.
The D-Bus interface XML is maintained in sync with it. Any new capability
requires:

1. An entry in `openapi.yaml`
2. A corresponding D-Bus method/signal in the XML
3. Implementation in the daemon handler
4. A CLI subcommand
5. UI in both QML and web frontends

This sequence is enforced by the definition of "done" for any feature.

### Event streaming

The daemon subscribes to the Incus event stream once and fans out to clients:

- **D-Bus**: emits signals on `org.KapsuleIncusManager` — QML and CLI `watch`
  commands subscribe to these
- **HTTP SSE**: `/api/v1/events` endpoint — web UI subscribes on page load
- **WebSocket**: `/api/v1/events/ws` — alternative for clients that prefer WS

All three receive the same event payloads, normalized from the raw Incus event
format into the PIP event schema.

### Terminal / console access

Interactive terminal access (exec into container, VM console) is proxied by
the daemon as a WebSocket endpoint:

```
/api/v1/containers/{name}/exec/ws
/api/v1/vms/{name}/console/ws
```

Both the web UI (xterm.js) and the QML UI (terminal widget) connect to these
endpoints. The CLI uses the Incus exec API directly via the daemon's D-Bus
`Exec` method, which returns a PTY file descriptor over D-Bus Unix FD passing.

---

## Feature Parity Contract

Every feature is available in QML UI, web UI, and CLI. The following domains
are in scope:

- **Containers**: full lifecycle, exec, file push/pull, snapshots, logs,
  resource limits, console
- **Virtual Machines**: same as containers plus VGA console
- **Networks**: list, create, edit, delete, VLAN management
- **Storage**: pools and volumes, full CRUD
- **Images**: browse remotes, pull, publish, delete, aliases
- **Profiles**: full CRUD, preset library (GPU, audio, display, ROCm, nesting)
- **Projects**: create, switch, configure, delete
- **Cluster**: node management, evacuation, roles
- **Remotes**: add, remove, switch, authenticate
- **App Containers**: deploy from Compose file, docker-compose import/convert,
  auto-reload on config change
- **Operations**: live log, cancel
- **Events**: real-time stream, filterable by type
- **Generic containers** (incusbox): create with cloud-init user setup, assemble
  (post-create packages + hooks), GPU/USB passthrough, port forwarding, snapshots,
  backups, fleet operations, publish
- **Waydroid containers**: provision with binder/ashmem setup, extension management
  (GApps, MicroG, Magisk, …), backup/restore, cloud sync, GPU passthrough, fleet
- **macOS VMs**: firmware/image download, VM creation with OVMF + OpenCore volumes,
  GPU passthrough, port forwarding, snapshots, backups, disk resize, fleet
- **Windows VMs**: VM creation from profile + ISO, guest tools, RemoteApp, winget
  app install, GPU passthrough, port forwarding, snapshots, backups, cloud sync,
  security hardening, disk resize, fleet

---

## Source Projects and Disposition

| Project | Role | What is taken |
|---|---|---|
| KDE/kapsule | Core architecture | Daemon structure, `libpenguins-incus-qt`, CLI patterns, D-Bus interface design |
| incus-ui-canonical | Web UI | React/TS app, adapted to PIP REST API |
| incus_container_manager | Reference | UX patterns and feature checklist for QML UI |
| incus_container_gui_setup | Assets | Incus profile YAML files, setup documentation |
| incus-app-container | Logic | App container provisioning, VLAN management, config schema |
| incus-compose | Reference | docker-compose → incus YAML mapping schema |
| nodegui | Dropped | Replaced by Qt6/QML |
| **incusbox** | **Merged** | **Generic container provisioning plugin + profiles** |
| **waydroid-toolkit** | **Merged** | **Waydroid provisioning plugin + Waydroid profile** |
| **Incus-MacOS-Toolkit** | **Merged** | **macOS VM provisioning plugin + macos-kvm profile** |
| **incus-windows-toolkit** | **Merged** | **Windows VM provisioning plugin + Windows profiles** |

### Provisioning plugin architecture

Each merged toolkit becomes a **provisioning plugin** — a Python module under
`daemon/penguins_incus/provisioning/` with a matching REST router under
`daemon/penguins_incus/api/rest/`. The plugin pattern follows the existing `compose.py`
plugin.

```
daemon/penguins_incus/provisioning/
  _base.py      shared helpers: cloud-init builder, device config builders
  compose.py    Docker Compose → Incus (existing)
  generic.py    incusbox: container create/assemble/gpu/usb/net/snapshot/fleet
  waydroid.py   waydroid-toolkit: container create/extensions/backup/gpu/fleet
  macos.py      Incus-MacOS-Toolkit: image/firmware/vm-create/snapshot/fleet
  windows.py    incus-windows-toolkit: vm-create/guest-tools/remoteapp/harden/fleet
```

**Key constraint**: plugins call `IncusClient` methods only — they never shell
out to `incus` CLI or any external tool. Operations that require running
commands inside a guest use `IncusClient.exec_instance()`. Operations that
require host-side downloads use a temporary helper container.

**IncusClient extensions** added to support the plugins:
- `exec_instance(name, command, environment)` — run command inside instance
- `push_file(name, path, content)` — write file into instance
- `pull_file(name, path)` — read file from instance
- `list_devices(name)` — get instance device dict
- `add_device(name, dev_name, config)` — add/replace device on instance
- `remove_device(name, dev_name)` — remove device from instance
- `get_host_resources()` — enumerate host GPU/USB hardware

---

## Licenses

| Component | License |
|---|---|
| daemon | GPL-3.0-or-later |
| libpenguins-incus-qt | LGPL-2.1-or-later |
| cli | GPL-3.0-or-later |
| ui-web | Apache-2.0 |
| ui-qml app | GPL-3.0-or-later |
| profiles | MIT |

---

## Non-Goals

- Windows or macOS *host* support (Incus is Linux-only; Windows/macOS *guests*
  are fully supported via the provisioning plugins)
- Managing non-Incus container runtimes (Docker, Podman) directly — only via
  app containers running inside Incus
- A mobile UI
- Replacing the `incus` CLI for scripting — the PIP CLI is a management
  companion, not a replacement for the upstream tool
- Maintaining the four source toolkits (incusbox, waydroid-toolkit,
  Incus-MacOS-Toolkit, incus-windows-toolkit) as independent projects — PIP is
  now the canonical location for all of their functionality
