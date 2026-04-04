"""REST routes for Waydroid container provisioning (waydroid-toolkit feature set)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request

from ...provisioning import waydroid as w

router = APIRouter(tags=["provisioning/waydroid"])


def _incus(req: Request) -> Any:  # type: ignore[return]
    return req.app.state.incus


# ── Container create ──────────────────────────────────────────────────────────

@router.post("/provisioning/waydroid", status_code=202)
async def create_waydroid_container(req: Request, body: dict[str, Any]) -> Any:
    """Provision an Incus container with Waydroid pre-installed."""
    return await w.create_waydroid_container(_incus(req), body)


# ── Extensions ────────────────────────────────────────────────────────────────

@router.get("/provisioning/waydroid/{name}/extensions")
async def list_extensions(req: Request, name: str,
                           project: str = "") -> Any:
    return await w.list_extensions(_incus(req), name, project=project)


@router.post("/provisioning/waydroid/{name}/extensions", status_code=202)
async def install_extension(req: Request, name: str,
                             body: dict[str, Any]) -> Any:
    return await w.install_extension(_incus(req), name, body)


@router.delete("/provisioning/waydroid/{name}/extensions/{extension}",
               status_code=202)
async def remove_extension(req: Request, name: str, extension: str,
                            project: str = "") -> Any:
    return await w.remove_extension(_incus(req), name,
                                     {"extension": extension,
                                      "project": project})


# ── Backup / restore ──────────────────────────────────────────────────────────

@router.get("/provisioning/waydroid/{name}/backups")
async def list_backups(req: Request, name: str, project: str = "") -> Any:
    return await w.list_backups(_incus(req), name, project=project)


@router.post("/provisioning/waydroid/{name}/backups", status_code=202)
async def backup_waydroid(req: Request, name: str,
                           body: dict[str, Any]) -> Any:
    return await w.backup_waydroid(_incus(req), name, body)


@router.post("/provisioning/waydroid/{name}/restore", status_code=202)
async def restore_waydroid(req: Request, name: str,
                            body: dict[str, Any]) -> Any:
    return await w.restore_waydroid(_incus(req), name, body)


# ── Cloud sync ────────────────────────────────────────────────────────────────

@router.put("/provisioning/waydroid/{name}/cloud-sync")
async def configure_cloud_sync(req: Request, name: str,
                                body: dict[str, Any]) -> Any:
    return await w.configure_cloud_sync(_incus(req), name, body)


# ── GPU ───────────────────────────────────────────────────────────────────────

@router.post("/provisioning/waydroid/{name}/gpus", status_code=202)
async def attach_gpu(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await w.attach_gpu(_incus(req), name, body)


@router.delete("/provisioning/waydroid/{name}/gpus/{dev_name}", status_code=202)
async def detach_gpu(req: Request, name: str, dev_name: str,
                     project: str = "") -> Any:
    return await w.detach_gpu(_incus(req), name, dev_name, project=project)


# ── Fleet ─────────────────────────────────────────────────────────────────────

@router.get("/provisioning/waydroid/fleet")
async def fleet_list(req: Request, project: str = "",
                     status: str = "") -> Any:
    return await w.fleet_list(_incus(req), project=project,
                               status_filter=status)


# ── Publish ───────────────────────────────────────────────────────────────────

@router.post("/provisioning/waydroid/publish", status_code=202)
async def publish_container(req: Request, body: dict[str, Any]) -> Any:
    return await w.publish_container(_incus(req), body)
