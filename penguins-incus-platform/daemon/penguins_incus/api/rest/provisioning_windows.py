"""REST routes for Windows VM provisioning (incus-windows-toolkit feature set)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request

from ...provisioning import windows as win

router = APIRouter(tags=["provisioning/windows"])


def _incus(req: Request) -> Any:
    return req.app.state.incus


# ── VM lifecycle ──────────────────────────────────────────────────────────────

@router.post("/provisioning/windows", status_code=202)
async def create_windows_vm(req: Request, body: dict[str, Any]) -> Any:
    """Create a Windows VM in Incus from a profile and optional ISO."""
    return await win.create_windows_vm(_incus(req), body)


@router.post("/provisioning/windows/{name}/start", status_code=202)
async def start_windows_vm(req: Request, name: str,
                            project: str = "") -> Any:
    return await win.start_windows_vm(_incus(req), name, project=project)


@router.post("/provisioning/windows/{name}/stop", status_code=202)
async def stop_windows_vm(req: Request, name: str,
                           force: bool = False, project: str = "") -> Any:
    return await win.stop_windows_vm(_incus(req), name, force=force,
                                      project=project)


# ── Snapshots ─────────────────────────────────────────────────────────────────

@router.get("/provisioning/windows/{name}/snapshots")
async def list_snapshots(req: Request, name: str,
                          project: str = "") -> Any:
    return await _incus(req).list_snapshots(name, project=project)


@router.post("/provisioning/windows/{name}/snapshots", status_code=202)
async def create_snapshot(req: Request, name: str,
                           body: dict[str, Any]) -> Any:
    return await _incus(req).create_snapshot(
        name, body["snapshot"],
        stateful=body.get("stateful", False),
        project=body.get("project", ""),
    )


@router.post("/provisioning/windows/{name}/snapshots/{snapshot}/restore",
             status_code=202)
async def restore_snapshot(req: Request, name: str, snapshot: str,
                            project: str = "") -> Any:
    return await _incus(req).restore_snapshot(name, snapshot, project=project)


@router.delete("/provisioning/windows/{name}/snapshots/{snapshot}",
               status_code=202)
async def delete_snapshot(req: Request, name: str, snapshot: str,
                           project: str = "") -> Any:
    return await _incus(req).delete_snapshot(name, snapshot, project=project)


@router.put("/provisioning/windows/{name}/snapshots/schedule")
async def set_snapshot_schedule(req: Request, name: str,
                                 body: dict[str, Any]) -> Any:
    return await win.set_snapshot_schedule(
        _incus(req), name,
        body["schedule"],
        expiry=body.get("expiry", ""),
        project=body.get("project", ""),
    )


# ── Backup / restore ──────────────────────────────────────────────────────────

@router.get("/provisioning/windows/{name}/backups")
async def list_backups(req: Request, name: str, project: str = "") -> Any:
    return await win.list_backups(_incus(req), name, project=project)


@router.post("/provisioning/windows/{name}/backups", status_code=202)
async def backup_vm(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await win.backup_vm(_incus(req), name, body)


@router.post("/provisioning/windows/{name}/restore", status_code=202)
async def restore_vm_backup(req: Request, name: str,
                             body: dict[str, Any]) -> Any:
    return await win.restore_vm_backup(_incus(req), name,
                                        body["backup_name"],
                                        project=body.get("project", ""))


# ── GPU ───────────────────────────────────────────────────────────────────────

@router.post("/provisioning/windows/{name}/gpus", status_code=202)
async def attach_gpu(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await win.attach_gpu(_incus(req), name, body)


@router.delete("/provisioning/windows/{name}/gpus/{dev_name}", status_code=202)
async def detach_gpu(req: Request, name: str, dev_name: str,
                     project: str = "") -> Any:
    return await win.detach_gpu(_incus(req), name, dev_name, project=project)


# ── Net port forwarding ───────────────────────────────────────────────────────

@router.post("/provisioning/windows/{name}/forwards", status_code=202)
async def add_forward(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await win.add_forward(_incus(req), name, body)


@router.delete("/provisioning/windows/{name}/forwards/{dev_name}",
               status_code=202)
async def remove_forward(req: Request, name: str, dev_name: str,
                          project: str = "") -> Any:
    return await win.remove_forward(_incus(req), name, dev_name,
                                     project=project)


# ── Guest tools ───────────────────────────────────────────────────────────────

@router.post("/provisioning/windows/{name}/guest-tools", status_code=202)
async def install_guest_tools(req: Request, name: str,
                               body: dict[str, Any]) -> Any:
    return await win.install_guest_tools(_incus(req), name, body)


# ── RemoteApp ─────────────────────────────────────────────────────────────────

@router.get("/provisioning/windows/{name}/remoteapp")
async def discover_remoteapps(req: Request, name: str,
                               project: str = "") -> Any:
    return await win.discover_remoteapps(_incus(req), name, project=project)


@router.post("/provisioning/windows/{name}/remoteapp/launch", status_code=202)
async def launch_remoteapp(req: Request, name: str,
                            body: dict[str, Any]) -> Any:
    return await win.launch_remoteapp(_incus(req), name, body)


# ── App store (winget) ────────────────────────────────────────────────────────

@router.post("/provisioning/windows/{name}/apps", status_code=202)
async def install_apps(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await win.install_apps(_incus(req), name, body)


# ── Cloud sync ────────────────────────────────────────────────────────────────

@router.put("/provisioning/windows/{name}/cloud-sync")
async def configure_cloud_sync(req: Request, name: str,
                                body: dict[str, Any]) -> Any:
    return await win.configure_cloud_sync(_incus(req), name, body)


# ── Security hardening ────────────────────────────────────────────────────────

@router.post("/provisioning/windows/{name}/harden", status_code=202)
async def harden_vm(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await win.harden_vm(_incus(req), name, body)


# ── Disk resize ───────────────────────────────────────────────────────────────

@router.post("/provisioning/windows/{name}/disk/resize", status_code=202)
async def resize_disk(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await win.resize_disk(_incus(req), name, body)


# ── Fleet ─────────────────────────────────────────────────────────────────────

@router.get("/provisioning/windows/fleet")
async def fleet_list(req: Request, project: str = "",
                     status: str = "") -> Any:
    return await win.fleet_list(_incus(req), project=project,
                                 status_filter=status)


@router.post("/provisioning/windows/fleet/start", status_code=202)
async def fleet_start(req: Request, body: dict[str, Any]) -> Any:
    return await win.fleet_start(_incus(req), body["names"],
                                  project=body.get("project", ""))


@router.post("/provisioning/windows/fleet/stop", status_code=202)
async def fleet_stop(req: Request, body: dict[str, Any]) -> Any:
    return await win.fleet_stop(_incus(req), body["names"],
                                 project=body.get("project", ""))


# ── Publish ───────────────────────────────────────────────────────────────────

@router.post("/provisioning/windows/publish", status_code=202)
async def publish_vm(req: Request, body: dict[str, Any]) -> Any:
    return await win.publish_vm(_incus(req), body)
