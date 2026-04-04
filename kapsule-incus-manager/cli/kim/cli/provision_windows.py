"""kim provision windows — Windows VM provisioning."""

from __future__ import annotations

import click


@click.group("windows")
def windows() -> None:
    """Windows VM provisioning (incus-windows-toolkit feature set)."""


@windows.command("create")
@click.option("--name", default="windows", show_default=True)
@click.option("--profile", default="windows-desktop", show_default=True)
@click.option("--image", default="", help="Path to Windows ISO.")
@click.option("--disk", default="", help="Path to additional disk image.")
@click.option("--ram", default="8GiB", show_default=True)
@click.option("--cpus", default=4, show_default=True, type=int)
@click.option("--disk-size", default="64GB", show_default=True)
@click.option("--gpu-overlay", default="", help="GPU overlay profile (vfio, looking-glass).")
@click.option("--rdp/--no-rdp", default=True, show_default=True)
@click.option("--autostart/--no-autostart", default=False)
@click.option("--project", default="")
@click.pass_context
def windows_create(ctx: click.Context, name: str, profile: str, image: str,
                   disk: str, ram: str, cpus: int, disk_size: str,
                   gpu_overlay: str, rdp: bool, autostart: bool,
                   project: str) -> None:
    """Create a Windows VM in Incus."""
    ctx.obj["client"].post("/api/v1/provisioning/windows", json={
        "name": name, "profile": profile, "image": image, "disk": disk,
        "ram": ram, "cpus": cpus, "disk_size": disk_size,
        "gpu_overlay": gpu_overlay, "rdp": rdp,
        "boot_autostart": autostart, "project": project,
    })


@windows.command("start")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def windows_start(ctx: click.Context, name: str, project: str) -> None:
    """Start a Windows VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/start",
                           params={"project": project}, json={})


@windows.command("stop")
@click.argument("name")
@click.option("--force/--no-force", default=False)
@click.option("--project", default="")
@click.pass_context
def windows_stop(ctx: click.Context, name: str, force: bool,
                  project: str) -> None:
    """Stop a Windows VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/stop",
                           params={"force": str(force).lower(),
                                   "project": project}, json={})


@windows.group("snapshot")
def windows_snapshot() -> None:
    """Snapshot management for Windows VMs."""


@windows_snapshot.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def win_snap_list(ctx: click.Context, name: str, project: str) -> None:
    """List snapshots."""
    ctx.obj["client"].get(f"/api/v1/provisioning/windows/{name}/snapshots",
                          params={"project": project})


@windows_snapshot.command("create")
@click.argument("name")
@click.argument("snapshot")
@click.option("--project", default="")
@click.pass_context
def win_snap_create(ctx: click.Context, name: str, snapshot: str,
                    project: str) -> None:
    """Create a snapshot."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/snapshots",
                           json={"snapshot": snapshot, "project": project})


@windows_snapshot.command("restore")
@click.argument("name")
@click.argument("snapshot")
@click.option("--project", default="")
@click.pass_context
def win_snap_restore(ctx: click.Context, name: str, snapshot: str,
                     project: str) -> None:
    """Restore a snapshot."""
    ctx.obj["client"].post(
        f"/api/v1/provisioning/windows/{name}/snapshots/{snapshot}/restore",
        params={"project": project}, json={})


@windows_snapshot.command("delete")
@click.argument("name")
@click.argument("snapshot")
@click.option("--project", default="")
@click.pass_context
def win_snap_delete(ctx: click.Context, name: str, snapshot: str,
                    project: str) -> None:
    """Delete a snapshot."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/windows/{name}/snapshots/{snapshot}",
        params={"project": project})


@windows_snapshot.command("schedule")
@click.argument("name")
@click.argument("schedule")
@click.option("--expiry", default="")
@click.option("--project", default="")
@click.pass_context
def win_snap_schedule(ctx: click.Context, name: str, schedule: str,
                      expiry: str, project: str) -> None:
    """Set automatic snapshot schedule."""
    ctx.obj["client"].put(
        f"/api/v1/provisioning/windows/{name}/snapshots/schedule",
        json={"schedule": schedule, "expiry": expiry, "project": project})


@windows.group("backup")
def windows_backup() -> None:
    """Backup and restore Windows VMs."""


@windows_backup.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def win_backup_list(ctx: click.Context, name: str, project: str) -> None:
    """List Incus backups."""
    ctx.obj["client"].get(f"/api/v1/provisioning/windows/{name}/backups",
                          params={"project": project})


@windows_backup.command("create")
@click.argument("name")
@click.option("--backup-name", default="")
@click.option("--instance-only/--no-instance-only", default=False)
@click.option("--project", default="")
@click.pass_context
def win_backup_create(ctx: click.Context, name: str, backup_name: str,
                      instance_only: bool, project: str) -> None:
    """Create an Incus backup of a Windows VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/backups", json={
        "backup_name": backup_name, "instance_only": instance_only,
        "project": project,
    })


@windows_backup.command("restore")
@click.argument("name")
@click.argument("backup_name")
@click.option("--project", default="")
@click.pass_context
def win_backup_restore(ctx: click.Context, name: str, backup_name: str,
                       project: str) -> None:
    """Restore a Windows VM from an Incus backup."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/restore",
                           json={"backup_name": backup_name, "project": project})


@windows.group("gpu")
def windows_gpu() -> None:
    """GPU passthrough for Windows VMs."""


@windows_gpu.command("attach")
@click.argument("name")
@click.option("--dev-name", default="gpu0", show_default=True)
@click.option("--type", "gpu_type", default="physical",
              type=click.Choice(["physical", "mdev", "mig", "virtio"]))
@click.option("--pci", default="")
@click.option("--project", default="")
@click.pass_context
def win_gpu_attach(ctx: click.Context, name: str, dev_name: str,
                   gpu_type: str, pci: str, project: str) -> None:
    """Attach a GPU to a Windows VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/gpus", json={
        "dev_name": dev_name, "gpu_type": gpu_type, "pci": pci,
        "project": project,
    })


@windows_gpu.command("detach")
@click.argument("name")
@click.argument("dev_name")
@click.option("--project", default="")
@click.pass_context
def win_gpu_detach(ctx: click.Context, name: str, dev_name: str,
                   project: str) -> None:
    """Detach a GPU from a Windows VM."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/windows/{name}/gpus/{dev_name}",
        params={"project": project})


@windows.group("net")
def windows_net() -> None:
    """Port-forward management for Windows VMs."""


@windows_net.command("forward")
@click.argument("name")
@click.option("--host-port", required=True, type=int)
@click.option("--guest-port", required=True, type=int)
@click.option("--protocol", default="tcp", show_default=True)
@click.option("--project", default="")
@click.pass_context
def win_net_forward(ctx: click.Context, name: str, host_port: int,
                    guest_port: int, protocol: str, project: str) -> None:
    """Add a port-forward proxy device."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/forwards", json={
        "host_port": host_port, "guest_port": guest_port,
        "protocol": protocol, "project": project,
    })


@windows_net.command("unforward")
@click.argument("name")
@click.argument("dev_name")
@click.option("--project", default="")
@click.pass_context
def win_net_unforward(ctx: click.Context, name: str, dev_name: str,
                      project: str) -> None:
    """Remove a port-forward proxy device."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/windows/{name}/forwards/{dev_name}",
        params={"project": project})


@windows.command("guest-tools")
@click.argument("name")
@click.option("--tool", "tools", multiple=True,
              type=click.Choice(["svcguest", "serviceman", "srvlib",
                                 "winbtrfs", "winfsp"]),
              help="Tool to install (repeatable).")
@click.option("--project", default="")
@click.pass_context
def windows_guest_tools(ctx: click.Context, name: str,
                         tools: tuple[str, ...], project: str) -> None:
    """Install Windows guest tools via PowerShell exec."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/guest-tools",
                           json={"tools": list(tools), "project": project})


@windows.group("remoteapp")
def windows_remoteapp() -> None:
    """Windows RemoteApp — run Windows apps as seamless Linux windows."""


@windows_remoteapp.command("discover")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def win_remoteapp_discover(ctx: click.Context, name: str, project: str) -> None:
    """Discover installed Windows applications."""
    ctx.obj["client"].get(f"/api/v1/provisioning/windows/{name}/remoteapp",
                          params={"project": project})


@windows_remoteapp.command("launch")
@click.argument("name")
@click.argument("app")
@click.argument("args", nargs=-1)
@click.option("--project", default="")
@click.pass_context
def win_remoteapp_launch(ctx: click.Context, name: str, app: str,
                          args: tuple[str, ...], project: str) -> None:
    """Launch a Windows application inside the VM."""
    ctx.obj["client"].post(
        f"/api/v1/provisioning/windows/{name}/remoteapp/launch",
        json={"app": app, "args": list(args), "project": project})


@windows.command("apps")
@click.argument("name")
@click.argument("app_ids", nargs=-1, required=True)
@click.option("--project", default="")
@click.pass_context
def windows_apps(ctx: click.Context, name: str, app_ids: tuple[str, ...],
                  project: str) -> None:
    """Install Windows applications via winget."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/apps",
                           json={"apps": list(app_ids), "project": project})


@windows.command("cloud-sync")
@click.argument("name")
@click.option("--remote-name", required=True)
@click.option("--remote-path", required=True)
@click.option("--schedule", default="")
@click.option("--project", default="")
@click.pass_context
def windows_cloud_sync(ctx: click.Context, name: str, remote_name: str,
                        remote_path: str, schedule: str, project: str) -> None:
    """Configure rclone cloud sync for Windows VM backups."""
    ctx.obj["client"].put(f"/api/v1/provisioning/windows/{name}/cloud-sync", json={
        "remote_name": remote_name, "remote_path": remote_path,
        "schedule": schedule, "project": project,
    })


@windows.command("harden")
@click.argument("name")
@click.option("--level", default="standard",
              type=click.Choice(["basic", "standard", "strict"]),
              show_default=True)
@click.option("--project", default="")
@click.pass_context
def windows_harden(ctx: click.Context, name: str, level: str,
                    project: str) -> None:
    """Apply security hardening to a Windows VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/harden",
                           json={"level": level, "project": project})


@windows.command("disk-resize")
@click.argument("name")
@click.argument("new_size")
@click.option("--project", default="")
@click.pass_context
def windows_disk_resize(ctx: click.Context, name: str, new_size: str,
                         project: str) -> None:
    """Resize the root disk of a Windows VM."""
    ctx.obj["client"].post(f"/api/v1/provisioning/windows/{name}/disk/resize",
                           json={"new_size": new_size, "project": project})


@windows.group("fleet")
def windows_fleet() -> None:
    """Bulk operations on Windows VMs."""


@windows_fleet.command("list")
@click.option("--project", default="")
@click.option("--status", default="")
@click.pass_context
def win_fleet_list(ctx: click.Context, project: str, status: str) -> None:
    """List Windows VMs."""
    ctx.obj["client"].get("/api/v1/provisioning/windows/fleet",
                          params={"project": project, "status": status})


@windows_fleet.command("start")
@click.argument("names", nargs=-1, required=True)
@click.option("--project", default="")
@click.pass_context
def win_fleet_start(ctx: click.Context, names: tuple[str, ...],
                    project: str) -> None:
    """Start multiple Windows VMs."""
    ctx.obj["client"].post("/api/v1/provisioning/windows/fleet/start",
                           json={"names": list(names), "project": project})


@windows_fleet.command("stop")
@click.argument("names", nargs=-1, required=True)
@click.option("--project", default="")
@click.pass_context
def win_fleet_stop(ctx: click.Context, names: tuple[str, ...],
                   project: str) -> None:
    """Stop multiple Windows VMs."""
    ctx.obj["client"].post("/api/v1/provisioning/windows/fleet/stop",
                           json={"names": list(names), "project": project})


@windows.command("publish")
@click.argument("name")
@click.option("--alias", default="")
@click.option("--description", default="")
@click.option("--public/--no-public", default=False)
@click.option("--project", default="")
@click.pass_context
def windows_publish(ctx: click.Context, name: str, alias: str,
                    description: str, public: bool, project: str) -> None:
    """Publish a Windows VM as a reusable Incus image."""
    ctx.obj["client"].post("/api/v1/provisioning/windows/publish", json={
        "name": name, "alias": alias, "description": description,
        "public": public, "project": project,
    })
