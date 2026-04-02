# Kapsule Incus Manager

Unified [Incus](https://linuxcontainers.org/incus/) container and VM management
with full feature parity across three frontends: a Qt6/QML desktop app, a React
web UI, and a CLI.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                     Frontends                           │
│  Qt6/QML desktop app  │  React web UI  │  kim CLI       │
└──────────┬────────────┴───────┬────────┴────────┬───────┘
           │ D-Bus              │ HTTP/WS/SSE      │ HTTP
           └──────────┬─────────┘                 │
                      ▼                            │
           ┌──────────────────────┐                │
           │    kim-daemon        │◄───────────────┘
           │  (FastAPI + dasbus)  │
           └──────────┬───────────┘
                      │ Unix socket
                      ▼
           ┌──────────────────────┐
           │       Incus          │
           │  (containers + VMs)  │
           └──────────────────────┘
```

The daemon is the single control plane. All three frontends are thin clients —
they never talk to Incus directly. The REST and D-Bus transports expose
identical operations, so every action available in the GUI is also available
in the CLI.

## Repository layout

```
├── ARCHITECTURE.md                    # Design decisions and component boundaries
├── kapsule-incus-manager/             # Main project
│   ├── api/schema/                    # OpenAPI schema + D-Bus XML (canonical)
│   ├── daemon/                        # Python daemon (FastAPI + dasbus)
│   ├── cli/                           # Python CLI (Click + httpx + rich)
│   ├── ui-web/                        # React/TypeScript web UI (Vite)
│   └── ui-qml/                        # Qt6/QML desktop UI + libkim-qt
```

Full documentation is in [`kapsule-incus-manager/README.md`](kapsule-incus-manager/README.md).

## Quick start

### Daemon

```bash
cd kapsule-incus-manager/daemon
pip install -e ".[dev]"
kim-daemon
```

### CLI

```bash
cd kapsule-incus-manager/cli
pip install -e ".[dev]"
kim container list
```

### Web UI

```bash
cd kapsule-incus-manager/ui-web
npm install && npm run dev
# Open http://localhost:5173
```

### QML desktop app

```bash
cmake -B build -S kapsule-incus-manager/ui-qml -G Ninja
cmake --build build
./build/kim-app
```

## Prerequisites

| Component | Requirement |
|---|---|
| Incus | ≥ 6.0 |
| Python | ≥ 3.11 |
| Node.js | ≥ 20 (web UI) |
| Qt6 | ≥ 6.5 with DBus, Network, WebSockets, Quick, QuickControls2 |
| CMake | ≥ 3.22 (QML app) |

## License

- Daemon, CLI, web UI: GPL-3.0-or-later
- `libkim-qt`: LGPL-2.1-or-later
