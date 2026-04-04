"""kim provision macos — macOS VM provisioning."""

from __future__ import annotations

import click


@click.group("macos")
def macos() -> None:
    """macOS VM provisioning (Incus-MacOS-Toolkit feature set)."""


@macos.group("image")
def macos_image() -> None:
    """macOS image management."""


@macos_image.command("firmware")
@click.option("--pool", "storage_pool", default="default", show_default=True)
@click.option("--project", default="")
@click.pass_context
def macos_image_firmware(ctx: click.Context, storage_pool: str,
                          project: str) -> None:
    """Download OVMF firmware and OpenCore via a helper container."""
    ctx.obj["client"].post("/api/v1/provisioning/macos/image/firmware",
                           json={"storage_pool": storage_pool, "project": project})


@macos_image.command("fetch")
@click.option("--version", default="sonoma", show_default=True)
@click.option("--pool", "storage_pool", default="default", show_default=True)
@click.option("--volume", "volume_name", default="")
@click.option("--project", default="")
@click.pass_context
def macos_image_fetch(ctx: click.Context, version: str, storage_pool: str,
                       volume_name: str, project: str) -> None:
    """Download macOS recovery image via a helper container."""
    ctx.obj["client"].post("/api/v1/provisioning/macos/image/fetch", json={
        "version": version, "storage_pool": storage_pool,
        "volume_name": volume_name, "project": project,
    })


@macos.command("create")
@click.argument("name")
@click.option("--version", default="sonoma", show_default=True)
@click.option("--ram", default="4GiB", show_default=True)
@click.option("--cpus", default=4, show_default=True, type=int)
@click.option("--pool", "storage_pool", default="default", show_default=True)
@click.option("--disk-vol", default="")
@click.option("--installer-vol", default="")
@click.option("--opencore-vol", default="")
@click.option("--project", default="")
@click.pass_context
def macos_create(ctx: click.Context, name: str, version: str, ram: str,
                  cpus: int, storage_pool: str, disk_vol: str,
                  installer_vol: str, opencore_vol: str, project: str) -> None:
    """Create a macOS VM with storage volumes attached."""
    ctx.obj["client"].post("/api/v1/provisioning/macos", json={
        "name": name, "version": version, "ram": ram, "cpus": cpus,
        "storage_pool": storage_pool,
        "disk_vol": disk_vol or f"{name}-disk",
        "installer_vol": installer_vol or f"{name}-installer",
        "opencore_vol": opencore_vol or f"{name}-opencore",
        "project": project,
    })


@macos.command("start")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def macos_start(ctx: click.Context, name: str, project: str) -> None:
    """Start a macOS VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/macos/{name}/start",
                           params={"project": project}, json={})


@macos.command("stop")
@click.argument("name")
@click.option("--force/--no-force", default=False)
@click.option("--project", default="")
@click.pass_context
def macos_stop(ctx: click.Context, name: str, force: bool, project: str) -> None:
    """Stop a macOS VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/macos/{name}/stop",
                           params={"force": str(force).lower(),
                                   "project": project}, json={})


@macos.group("snapshot")
def macos_snapshot() -> None:
    """Snapshot management for macOS VMs."""


@macos_snapshot.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def macos_snap_list(ctx: click.Context, name: str, project: str) -> None:
    """List snapshots."""
    ctx.obj["client"].get(f"/api/v1/provisioning/macos/{name}/snapshots",
                          params={"project": project})


@macos_snapshot.command("create")
@click.argument("name")
@click.argument("snapshot")
@click.option("--project", default="")
@click.pass_context
def macos_snap_create(ctx: click.Context, name: str, snapshot: str,
                       project: str) -> None:
    """Create a snapshot."""
    ctx.obj["client"].post(f"/api/v1/provisioning/macos/{name}/snapshots",
                           json={"snapshot": snapshot, "project": project})


@macos_snapshot.command("restore")
@click.argument("name")
@click.argument("snapshot")
@click.option("--project", default="")
@click.pass_context
def macos_snap_restore(ctx: click.Context, name: str, snapshot: str,
                        project: str) -> None:
    """Restore a snapshot."""
    ctx.obj["client"].post(
        f"/api/v1/provisioning/macos/{name}/snapshots/{snapshot}/restore",
        params={"project": project}, json={})


@macos_snapshot.command("delete")
@click.argument("name")
@click.argument("snapshot")
@click.option("--project", default="")
@click.pass_context
def macos_snap_delete(ctx: click.Context, name: str, snapshot: str,
                       project: str) -> None:
    """Delete a snapshot."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/macos/{name}/snapshots/{snapshot}",
        params={"project": project})


@macos_snapshot.command("schedule")
@click.argument("name")
@click.argument("schedule")
@click.option("--expiry", default="")
@click.option("--project", default="")
@click.pass_context
def macos_snap_schedule(ctx: click.Context, name: str, schedule: str,
                         expiry: str, project: str) -> None:
    """Set automatic snapshot schedule."""
    ctx.obj["client"].put(
        f"/api/v1/provisioning/macos/{name}/snapshots/schedule",
        json={"schedule": schedule, "expiry": expiry, "project": project})


@macos.group("backup")
def macos_backup() -> None:
    """Backup and restore macOS VMs."""


@macos_backup.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def macos_backup_list(ctx: click.Context, name: str, project: str) -> None:
    """List Incus backups."""
    ctx.obj["client"].get(f"/api/v1/provisioning/macos/{name}/backups",
                          params={"project": project})


@macos_backup.command("create")
@click.argument("name")
@click.option("--backup-name", default="")
@click.option("--instance-only/--no-instance-only", default=False)
@click.option("--project", default="")
@click.pass_context
def macos_backup_create(ctx: click.Context, name: str, backup_name: str,
                         instance_only: bool, project: str) -> None:
    """Create an Incus backup of a macOS VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/macos/{name}/backups", json={
        "backup_name": backup_name, "instance_only": instance_only,
        "project": project,
    })


@macos_backup.command("restore")
@click.argument("name")
@click.argument("backup_name")
@click.option("--project", default="")
@click.pass_context
def macos_backup_restore(ctx: click.Context, name: str, backup_name: str,
                          project: str) -> None:
    """Restore a macOS VM from an Incus backup."""
    ctx.obj["client"].post(f"/api/v1/provisioning/macos/{name}/restore",
                           json={"backup_name": backup_name, "project": project})


@macos.group("gpu")
def macos_gpu() -> None:
    """GPU passthrough for macOS VMs."""


@macos_gpu.command("attach")
@click.argument("name")
@click.option("--dev-name", default="gpu0", show_default=True)
@click.option("--pci", default="")
@click.option("--project", default="")
@click.pass_context
def macos_gpu_attach(ctx: click.Context, name: str, dev_name: str,
                      pci: str, project: str) -> None:
    """Attach a GPU to a macOS VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/macos/{name}/gpus", json={
        "dev_name": dev_name, "pci": pci, "project": project,
    })


@macos_gpu.command("detach")
@click.argument("name")
@click.argument("dev_name")
@click.option("--project", default="")
@click.pass_context
def macos_gpu_detach(ctx: click.Context, name: str, dev_name: str,
                      project: str) -> None:
    """Detach a GPU from a macOS VM."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/macos/{name}/gpus/{dev_name}",
        params={"project": project})


@macos.group("net")
def macos_net() -> None:
    """Port-forward management for macOS VMs."""


@macos_net.command("forward")
@click.argument("name")
@click.option("--host-port", required=True, type=int)
@click.option("--guest-port", required=True, type=int)
@click.option("--protocol", default="tcp", show_default=True)
@click.option("--project", default="")
@click.pass_context
def macos_net_forward(ctx: click.Context, name: str, host_port: int,
                       guest_port: int, protocol: str, project: str) -> None:
    """Add a port-forward proxy device."""
    ctx.obj["client"].post(f"/api/v1/provisioning/macos/{name}/forwards", json={
        "host_port": host_port, "guest_port": guest_port,
        "protocol": protocol, "project": project,
    })


@macos_net.command("unforward")
@click.argument("name")
@click.argument("dev_name")
@click.option("--project", default="")
@click.pass_context
def macos_net_unforward(ctx: click.Context, name: str, dev_name: str,
                         project: str) -> None:
    """Remove a port-forward proxy device."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/macos/{name}/forwards/{dev_name}",
        params={"project": project})


@macos.command("disk-resize")
@click.argument("name")
@click.argument("new_size")
@click.option("--pool", "storage_pool", default="default", show_default=True)
@click.option("--volume", "volume_name", default="")
@click.option("--project", default="")
@click.pass_context
def macos_disk_resize(ctx: click.Context, name: str, new_size: str,
                       storage_pool: str, volume_name: str, project: str) -> None:
    """Resize the macOS VM disk volume."""
    ctx.obj["client"].post(f"/api/v1/provisioning/macos/{name}/disk/resize", json={
        "new_size": new_size, "storage_pool": storage_pool,
        "volume_name": volume_name or f"{name}-disk", "project": project,
    })


@macos.group("fleet")
def macos_fleet() -> None:
    """Bulk operations on macOS VMs."""


@macos_fleet.command("list")
@click.option("--project", default="")
@click.option("--status", default="")
@click.pass_context
def macos_fleet_list(ctx: click.Context, project: str, status: str) -> None:
    """List macOS VMs."""
    ctx.obj["client"].get("/api/v1/provisioning/macos/fleet",
                          params={"project": project, "status": status})


@macos_fleet.command("start")
@click.argument("names", nargs=-1, required=True)
@click.option("--project", default="")
@click.pass_context
def macos_fleet_start(ctx: click.Context, names: tuple[str, ...],
                       project: str) -> None:
    """Start multiple macOS VMs."""
    ctx.obj["client"].post("/api/v1/provisioning/macos/fleet/start",
                           json={"names": list(names), "project": project})


@macos_fleet.command("stop")
@click.argument("names", nargs=-1, required=True)
@click.option("--project", default="")
@click.pass_context
def macos_fleet_stop(ctx: click.Context, names: tuple[str, ...],
                      project: str) -> None:
    """Stop multiple macOS VMs."""
    ctx.obj["client"].post("/api/v1/provisioning/macos/fleet/stop",
                           json={"names": list(names), "project": project})


@macos.command("publish")
@click.argument("name")
@click.option("--alias", default="")
@click.option("--description", default="")
@click.option("--public/--no-public", default=False)
@click.option("--project", default="")
@click.pass_context
def macos_publish(ctx: click.Context, name: str, alias: str,
                   description: str, public: bool, project: str) -> None:
    """Publish a macOS VM as a reusable Incus image."""
    ctx.obj["client"].post("/api/v1/provisioning/macos/publish", json={
        "name": name, "alias": alias, "description": description,
        "public": public, "project": project,
    })
