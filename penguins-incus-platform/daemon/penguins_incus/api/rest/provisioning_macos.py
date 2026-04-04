"""REST routes for macOS VM provisioning (Incus-MacOS-Toolkit feature set)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request

from ...provisioning import macos as m

router = APIRouter(tags=["provisioning/macos"])


def _incus(req: Request) -> Any:  # type: ignore[return]
    return req.app.state.incus


# ── Image management ──────────────────────────────────────────────────────────

@router.post("/provisioning/macos/image/firmware", status_code=202)
async def download_firmware(req: Request, body: dict[str, Any]) -> Any:
    """Download OVMF firmware and OpenCore into Incus storage volumes."""
    return await m.download_firmware(_incus(req), body)


@router.post("/provisioning/macos/image/fetch", status_code=202)
async def fetch_macos_image(req: Request, body: dict[str, Any]) -> Any:
    """Trigger macOS recovery image download via a helper container."""
    return await m.fetch_macos_image(_incus(req), body)


# ── VM lifecycle ──────────────────────────────────────────────────────────────

@router.post("/provisioning/macos", status_code=202)
async def create_macos_vm(req: Request, body: dict[str, Any]) -> Any:
    """Create a macOS VM with all required storage volumes attached."""
    return await m.create_macos_vm(_incus(req), body)


@router.post("/provisioning/macos/{name}/start", status_code=202)
async def start_macos_vm(req: Request, name: str,
                          project: str = "") -> Any:
    return await m.start_macos_vm(_incus(req), name, project=project)


@router.post("/provisioning/macos/{name}/stop", status_code=202)
async def stop_macos_vm(req: Request, name: str,
                         force: bool = False, project: str = "") -> Any:
    return await m.stop_macos_vm(_incus(req), name, force=force,
                                  project=project)


# ── Snapshots ─────────────────────────────────────────────────────────────────

@router.get("/provisioning/macos/{name}/snapshots")
async def list_snapshots(req: Request, name: str,
                          project: str = "") -> Any:
    return await _incus(req).list_snapshots(name, project=project)


@router.post("/provisioning/macos/{name}/snapshots", status_code=202)
async def create_snapshot(req: Request, name: str,
                           body: dict[str, Any]) -> Any:
    return await _incus(req).create_snapshot(
        name, body["snapshot"],
        stateful=body.get("stateful", False),
        project=body.get("project", ""),
    )


@router.post("/provisioning/macos/{name}/snapshots/{snapshot}/restore",
             status_code=202)
async def restore_snapshot(req: Request, name: str, snapshot: str,
                            project: str = "") -> Any:
    return await _incus(req).restore_snapshot(name, snapshot, project=project)


@router.delete("/provisioning/macos/{name}/snapshots/{snapshot}",
               status_code=202)
async def delete_snapshot(req: Request, name: str, snapshot: str,
                           project: str = "") -> Any:
    return await _incus(req).delete_snapshot(name, snapshot, project=project)


@router.put("/provisioning/macos/{name}/snapshots/schedule")
async def set_snapshot_schedule(req: Request, name: str,
                                 body: dict[str, Any]) -> Any:
    return await m.set_snapshot_schedule(
        _incus(req), name,
        body["schedule"],
        expiry=body.get("expiry", ""),
        project=body.get("project", ""),
    )


# ── Backup / restore ──────────────────────────────────────────────────────────

@router.get("/provisioning/macos/{name}/backups")
async def list_backups(req: Request, name: str, project: str = "") -> Any:
    return await m.list_backups(_incus(req), name, project=project)


@router.post("/provisioning/macos/{name}/backups", status_code=202)
async def backup_vm(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await m.backup_vm(_incus(req), name, body)


@router.post("/provisioning/macos/{name}/restore", status_code=202)
async def restore_vm_backup(req: Request, name: str,
                             body: dict[str, Any]) -> Any:
    return await m.restore_vm_backup(_incus(req), name,
                                      body["backup_name"],
                                      project=body.get("project", ""))


# ── GPU ───────────────────────────────────────────────────────────────────────

@router.post("/provisioning/macos/{name}/gpus", status_code=202)
async def attach_gpu(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await m.attach_gpu(_incus(req), name, body)


@router.delete("/provisioning/macos/{name}/gpus/{dev_name}", status_code=202)
async def detach_gpu(req: Request, name: str, dev_name: str,
                     project: str = "") -> Any:
    return await m.detach_gpu(_incus(req), name, dev_name, project=project)


# ── Net port forwarding ───────────────────────────────────────────────────────

@router.post("/provisioning/macos/{name}/forwards", status_code=202)
async def add_forward(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await m.add_forward(_incus(req), name, body)


@router.delete("/provisioning/macos/{name}/forwards/{dev_name}",
               status_code=202)
async def remove_forward(req: Request, name: str, dev_name: str,
                          project: str = "") -> Any:
    return await m.remove_forward(_incus(req), name, dev_name, project=project)


# ── Disk resize ───────────────────────────────────────────────────────────────

@router.post("/provisioning/macos/{name}/disk/resize", status_code=202)
async def resize_disk(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await m.resize_disk(_incus(req), name, body)


# ── Fleet ─────────────────────────────────────────────────────────────────────

@router.get("/provisioning/macos/fleet")
async def fleet_list(req: Request, project: str = "",
                     status: str = "") -> Any:
    return await m.fleet_list(_incus(req), project=project,
                               status_filter=status)


@router.post("/provisioning/macos/fleet/start", status_code=202)
async def fleet_start(req: Request, body: dict[str, Any]) -> Any:
    return await m.fleet_start(_incus(req), body["names"],
                                project=body.get("project", ""))


@router.post("/provisioning/macos/fleet/stop", status_code=202)
async def fleet_stop(req: Request, body: dict[str, Any]) -> Any:
    return await m.fleet_stop(_incus(req), body["names"],
                               project=body.get("project", ""))


# ── Publish ───────────────────────────────────────────────────────────────────

@router.post("/provisioning/macos/publish", status_code=202)
async def publish_vm(req: Request, body: dict[str, Any]) -> Any:
    return await m.publish_vm(_incus(req), body)
