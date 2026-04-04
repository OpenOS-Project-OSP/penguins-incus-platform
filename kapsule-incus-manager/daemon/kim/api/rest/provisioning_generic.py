"""REST routes for generic container provisioning (incusbox feature set)."""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Request

from ...provisioning import generic as g

router = APIRouter(tags=["provisioning/generic"])


def _incus(req: Request) -> Any:  # type: ignore[return]
    return req.app.state.incus


# ── Container lifecycle ───────────────────────────────────────────────────────

@router.post("/provisioning/generic", status_code=202)
async def create_container(req: Request, body: dict[str, Any]) -> Any:
    """Create an incusbox-style container with cloud-init user setup."""
    return await g.create_container(_incus(req), body)


@router.post("/provisioning/generic/{name}/assemble", status_code=202)
async def assemble_container(req: Request, name: str,
                              body: dict[str, Any]) -> Any:
    """Run post-create assembly steps (packages, hooks, shell integration)."""
    return await g.assemble_container(_incus(req), name, body)


# ── Snapshots ─────────────────────────────────────────────────────────────────

@router.get("/provisioning/generic/{name}/snapshots")
async def list_snapshots(req: Request, name: str,
                          project: str = "") -> Any:
    return await g.list_snapshots(_incus(req), name, project=project)


@router.post("/provisioning/generic/{name}/snapshots", status_code=202)
async def create_snapshot(req: Request, name: str,
                           body: dict[str, Any]) -> Any:
    return await g.create_snapshot(
        _incus(req), name,
        body["snapshot"],
        stateful=body.get("stateful", False),
        project=body.get("project", ""),
    )


@router.post("/provisioning/generic/{name}/snapshots/{snapshot}/restore",
             status_code=202)
async def restore_snapshot(req: Request, name: str, snapshot: str,
                            project: str = "") -> Any:
    return await g.restore_snapshot(_incus(req), name, snapshot,
                                     project=project)


@router.delete("/provisioning/generic/{name}/snapshots/{snapshot}",
               status_code=202)
async def delete_snapshot(req: Request, name: str, snapshot: str,
                           project: str = "") -> Any:
    return await g.delete_snapshot(_incus(req), name, snapshot,
                                    project=project)


@router.put("/provisioning/generic/{name}/snapshots/schedule")
async def set_snapshot_schedule(req: Request, name: str,
                                 body: dict[str, Any]) -> Any:
    return await g.set_snapshot_schedule(
        _incus(req), name,
        body["schedule"],
        expiry=body.get("expiry", ""),
        project=body.get("project", ""),
    )


@router.delete("/provisioning/generic/{name}/snapshots/schedule")
async def disable_snapshot_schedule(req: Request, name: str,
                                     project: str = "") -> Any:
    return await g.disable_snapshot_schedule(_incus(req), name,
                                              project=project)


# ── GPU ───────────────────────────────────────────────────────────────────────

@router.get("/provisioning/generic/host/gpus")
async def list_host_gpus(req: Request) -> Any:
    return await g.list_host_gpus(_incus(req))


@router.get("/provisioning/generic/{name}/gpus")
async def list_instance_gpus(req: Request, name: str,
                              project: str = "") -> Any:
    return await g.list_instance_gpus(_incus(req), name, project=project)


@router.post("/provisioning/generic/{name}/gpus", status_code=202)
async def attach_gpu(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await g.attach_gpu(_incus(req), name, body)


@router.delete("/provisioning/generic/{name}/gpus/{dev_name}", status_code=202)
async def detach_gpu(req: Request, name: str, dev_name: str,
                     project: str = "") -> Any:
    return await g.detach_gpu(_incus(req), name, dev_name, project=project)


# ── USB ───────────────────────────────────────────────────────────────────────

@router.get("/provisioning/generic/host/usb")
async def list_host_usb(req: Request) -> Any:
    return await g.list_host_usb(_incus(req))


@router.get("/provisioning/generic/{name}/usb")
async def list_instance_usb(req: Request, name: str,
                             project: str = "") -> Any:
    return await g.list_instance_usb(_incus(req), name, project=project)


@router.post("/provisioning/generic/{name}/usb", status_code=202)
async def attach_usb(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await g.attach_usb(_incus(req), name, body)


@router.delete("/provisioning/generic/{name}/usb/{dev_name}", status_code=202)
async def detach_usb(req: Request, name: str, dev_name: str,
                     project: str = "") -> Any:
    return await g.detach_usb(_incus(req), name, dev_name, project=project)


# ── Network port forwarding ───────────────────────────────────────────────────

@router.get("/provisioning/generic/{name}/forwards")
async def list_forwards(req: Request, name: str, project: str = "") -> Any:
    return await g.list_forwards(_incus(req), name, project=project)


@router.post("/provisioning/generic/{name}/forwards", status_code=202)
async def add_forward(req: Request, name: str, body: dict[str, Any]) -> Any:
    return await g.add_forward(_incus(req), name, body)


@router.delete("/provisioning/generic/{name}/forwards/{dev_name}",
               status_code=202)
async def remove_forward(req: Request, name: str, dev_name: str,
                          project: str = "") -> Any:
    return await g.remove_forward(_incus(req), name, dev_name, project=project)


# ── Fleet ─────────────────────────────────────────────────────────────────────

@router.get("/provisioning/generic/fleet")
async def fleet_list(req: Request, project: str = "",
                     status: str = "") -> Any:
    return await g.fleet_list(_incus(req), project=project,
                               status_filter=status)


@router.post("/provisioning/generic/fleet/start", status_code=202)
async def fleet_start(req: Request, body: dict[str, Any]) -> Any:
    return await g.fleet_start(_incus(req), body["names"],
                                project=body.get("project", ""))


@router.post("/provisioning/generic/fleet/stop", status_code=202)
async def fleet_stop(req: Request, body: dict[str, Any]) -> Any:
    return await g.fleet_stop(_incus(req), body["names"],
                               project=body.get("project", ""))


# ── Publish ───────────────────────────────────────────────────────────────────

@router.post("/provisioning/generic/publish", status_code=202)
async def publish_container(req: Request, body: dict[str, Any]) -> Any:
    return await g.publish_container(_incus(req), body)
