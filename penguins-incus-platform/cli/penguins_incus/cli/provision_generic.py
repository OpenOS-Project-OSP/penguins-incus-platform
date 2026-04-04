"""penguins-incus provision generic — incusbox-style container provisioning."""

from __future__ import annotations

import click


@click.group("generic")
def generic() -> None:
    """Generic container provisioning (incusbox feature set)."""


@generic.command("create")
@click.argument("name")
@click.option("--image", default="images:ubuntu/24.04/cloud", show_default=True)
@click.option("--user", "user_name", default="user", show_default=True)
@click.option("--package", "packages", multiple=True, help="Extra packages (repeatable).")
@click.option("--nvidia/--no-nvidia", default=False)
@click.option("--profile", multiple=True)
@click.option("--disk-size", default="20GB", show_default=True)
@click.option("--volume", "volumes", multiple=True, help="src:dst[:ro] (repeatable).")
@click.option("--project", default="")
@click.pass_context
def generic_create(ctx: click.Context, name: str, image: str, user_name: str,
                   packages: tuple[str, ...], nvidia: bool,
                   profile: tuple[str, ...], disk_size: str,
                   volumes: tuple[str, ...], project: str) -> None:
    """Create an incusbox-style container."""
    ctx.obj["client"].post("/api/v1/provisioning/generic", json={
        "name": name, "image": image, "user_name": user_name,
        "additional_packages": list(packages), "nvidia": nvidia,
        "profiles": list(profile) or ["default"],
        "disk_size": disk_size, "volumes": list(volumes), "project": project,
    })


@generic.command("assemble")
@click.argument("name")
@click.option("--package", "packages", multiple=True)
@click.option("--hook", "hooks", multiple=True)
@click.option("--no-shell-integration", "shell_integration", flag_value=False, default=True)
@click.option("--project", default="")
@click.pass_context
def generic_assemble(ctx: click.Context, name: str, packages: tuple[str, ...],
                     hooks: tuple[str, ...], shell_integration: bool,
                     project: str) -> None:
    """Run post-create assembly steps inside a container."""
    ctx.obj["client"].post(f"/api/v1/provisioning/generic/{name}/assemble", json={
        "packages": list(packages), "hooks": list(hooks),
        "shell_integration": shell_integration, "project": project,
    })


@generic.group("gpu")
def generic_gpu() -> None:
    """GPU passthrough for containers."""


@generic_gpu.command("list-host")
@click.pass_context
def generic_gpu_list_host(ctx: click.Context) -> None:
    """List GPUs available on the host."""
    ctx.obj["client"].get("/api/v1/provisioning/generic/host/gpus")


@generic_gpu.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def generic_gpu_list(ctx: click.Context, name: str, project: str) -> None:
    """List GPUs attached to a container."""
    ctx.obj["client"].get(f"/api/v1/provisioning/generic/{name}/gpus",
                          params={"project": project})


@generic_gpu.command("attach")
@click.argument("name")
@click.option("--dev-name", default="gpu0", show_default=True)
@click.option("--type", "gpu_type", default="physical",
              type=click.Choice(["physical", "mdev", "mig", "virtio"]))
@click.option("--pci", default="")
@click.option("--vendor", default="")
@click.option("--project", default="")
@click.pass_context
def generic_gpu_attach(ctx: click.Context, name: str, dev_name: str,
                       gpu_type: str, pci: str, vendor: str, project: str) -> None:
    """Attach a GPU to a container."""
    ctx.obj["client"].post(f"/api/v1/provisioning/generic/{name}/gpus", json={
        "dev_name": dev_name, "gpu_type": gpu_type,
        "pci": pci, "vendor": vendor, "project": project,
    })


@generic_gpu.command("detach")
@click.argument("name")
@click.argument("dev_name")
@click.option("--project", default="")
@click.pass_context
def generic_gpu_detach(ctx: click.Context, name: str, dev_name: str,
                       project: str) -> None:
    """Detach a GPU from a container."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/generic/{name}/gpus/{dev_name}",
        params={"project": project})


@generic.group("usb")
def generic_usb() -> None:
    """USB passthrough for containers."""


@generic_usb.command("list-host")
@click.pass_context
def generic_usb_list_host(ctx: click.Context) -> None:
    """List USB devices available on the host."""
    ctx.obj["client"].get("/api/v1/provisioning/generic/host/usb")


@generic_usb.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def generic_usb_list(ctx: click.Context, name: str, project: str) -> None:
    """List USB devices attached to a container."""
    ctx.obj["client"].get(f"/api/v1/provisioning/generic/{name}/usb",
                          params={"project": project})


@generic_usb.command("attach")
@click.argument("name")
@click.option("--vendor-id", required=True)
@click.option("--product-id", required=True)
@click.option("--dev-name", default="usb0", show_default=True)
@click.option("--project", default="")
@click.pass_context
def generic_usb_attach(ctx: click.Context, name: str, vendor_id: str,
                       product_id: str, dev_name: str, project: str) -> None:
    """Attach a USB device to a container."""
    ctx.obj["client"].post(f"/api/v1/provisioning/generic/{name}/usb", json={
        "vendor_id": vendor_id, "product_id": product_id,
        "dev_name": dev_name, "project": project,
    })


@generic_usb.command("detach")
@click.argument("name")
@click.argument("dev_name")
@click.option("--project", default="")
@click.pass_context
def generic_usb_detach(ctx: click.Context, name: str, dev_name: str,
                       project: str) -> None:
    """Detach a USB device from a container."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/generic/{name}/usb/{dev_name}",
        params={"project": project})


@generic.group("net")
def generic_net() -> None:
    """Port-forward management for containers."""


@generic_net.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def generic_net_list(ctx: click.Context, name: str, project: str) -> None:
    """List port-forward proxy devices on a container."""
    ctx.obj["client"].get(f"/api/v1/provisioning/generic/{name}/forwards",
                          params={"project": project})


@generic_net.command("forward")
@click.argument("name")
@click.option("--host-port", required=True, type=int)
@click.option("--guest-port", required=True, type=int)
@click.option("--protocol", default="tcp", show_default=True)
@click.option("--listen", "listen_addr", default="127.0.0.1", show_default=True)
@click.option("--project", default="")
@click.pass_context
def generic_net_forward(ctx: click.Context, name: str, host_port: int,
                        guest_port: int, protocol: str, listen_addr: str,
                        project: str) -> None:
    """Add a port-forward proxy device."""
    ctx.obj["client"].post(f"/api/v1/provisioning/generic/{name}/forwards", json={
        "host_port": host_port, "guest_port": guest_port,
        "protocol": protocol, "listen_addr": listen_addr, "project": project,
    })


@generic_net.command("unforward")
@click.argument("name")
@click.argument("dev_name")
@click.option("--project", default="")
@click.pass_context
def generic_net_unforward(ctx: click.Context, name: str, dev_name: str,
                           project: str) -> None:
    """Remove a port-forward proxy device."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/generic/{name}/forwards/{dev_name}",
        params={"project": project})


@generic.group("snapshot")
def generic_snapshot() -> None:
    """Snapshot management for containers."""


@generic_snapshot.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def generic_snap_list(ctx: click.Context, name: str, project: str) -> None:
    """List snapshots."""
    ctx.obj["client"].get(f"/api/v1/provisioning/generic/{name}/snapshots",
                          params={"project": project})


@generic_snapshot.command("create")
@click.argument("name")
@click.argument("snapshot")
@click.option("--stateful/--no-stateful", default=False)
@click.option("--project", default="")
@click.pass_context
def generic_snap_create(ctx: click.Context, name: str, snapshot: str,
                        stateful: bool, project: str) -> None:
    """Create a snapshot."""
    ctx.obj["client"].post(f"/api/v1/provisioning/generic/{name}/snapshots",
                           json={"snapshot": snapshot, "stateful": stateful,
                                 "project": project})


@generic_snapshot.command("restore")
@click.argument("name")
@click.argument("snapshot")
@click.option("--project", default="")
@click.pass_context
def generic_snap_restore(ctx: click.Context, name: str, snapshot: str,
                          project: str) -> None:
    """Restore a snapshot."""
    ctx.obj["client"].post(
        f"/api/v1/provisioning/generic/{name}/snapshots/{snapshot}/restore",
        params={"project": project}, json={})


@generic_snapshot.command("delete")
@click.argument("name")
@click.argument("snapshot")
@click.option("--project", default="")
@click.pass_context
def generic_snap_delete(ctx: click.Context, name: str, snapshot: str,
                         project: str) -> None:
    """Delete a snapshot."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/generic/{name}/snapshots/{snapshot}",
        params={"project": project})


@generic_snapshot.command("schedule")
@click.argument("name")
@click.argument("schedule")
@click.option("--expiry", default="")
@click.option("--project", default="")
@click.pass_context
def generic_snap_schedule(ctx: click.Context, name: str, schedule: str,
                           expiry: str, project: str) -> None:
    """Set automatic snapshot schedule (e.g. '@daily')."""
    ctx.obj["client"].put(
        f"/api/v1/provisioning/generic/{name}/snapshots/schedule",
        json={"schedule": schedule, "expiry": expiry, "project": project})


@generic_snapshot.command("schedule-disable")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def generic_snap_schedule_disable(ctx: click.Context, name: str,
                                   project: str) -> None:
    """Disable automatic snapshots."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/generic/{name}/snapshots/schedule",
        params={"project": project})


@generic.group("fleet")
def generic_fleet() -> None:
    """Bulk operations on containers."""


@generic_fleet.command("list")
@click.option("--project", default="")
@click.option("--status", default="")
@click.pass_context
def generic_fleet_list(ctx: click.Context, project: str, status: str) -> None:
    """List all containers."""
    ctx.obj["client"].get("/api/v1/provisioning/generic/fleet",
                          params={"project": project, "status": status})


@generic_fleet.command("start")
@click.argument("names", nargs=-1, required=True)
@click.option("--project", default="")
@click.pass_context
def generic_fleet_start(ctx: click.Context, names: tuple[str, ...],
                         project: str) -> None:
    """Start multiple containers."""
    ctx.obj["client"].post("/api/v1/provisioning/generic/fleet/start",
                           json={"names": list(names), "project": project})


@generic_fleet.command("stop")
@click.argument("names", nargs=-1, required=True)
@click.option("--project", default="")
@click.pass_context
def generic_fleet_stop(ctx: click.Context, names: tuple[str, ...],
                        project: str) -> None:
    """Stop multiple containers."""
    ctx.obj["client"].post("/api/v1/provisioning/generic/fleet/stop",
                           json={"names": list(names), "project": project})


@generic.command("publish")
@click.argument("name")
@click.option("--alias", default="")
@click.option("--description", default="")
@click.option("--public/--no-public", default=False)
@click.option("--project", default="")
@click.pass_context
def generic_publish(ctx: click.Context, name: str, alias: str,
                    description: str, public: bool, project: str) -> None:
    """Publish a container as a reusable Incus image."""
    ctx.obj["client"].post("/api/v1/provisioning/generic/publish", json={
        "name": name, "alias": alias, "description": description,
        "public": public, "project": project,
    })
