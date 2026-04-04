"""penguins-incus provision waydroid — Waydroid container provisioning."""

from __future__ import annotations

import click


@click.group("waydroid")
def waydroid() -> None:
    """Waydroid Android container provisioning."""


@waydroid.command("create")
@click.argument("name")
@click.option("--image", default="images:ubuntu/22.04/cloud", show_default=True)
@click.option("--image-type", default="VANILLA",
              type=click.Choice(["VANILLA", "GAPPS"]), show_default=True)
@click.option("--arch", default="x86_64",
              type=click.Choice(["x86_64", "arm64"]), show_default=True)
@click.option("--gpu/--no-gpu", default=False)
@click.option("--disk-size", default="40GB", show_default=True)
@click.option("--project", default="")
@click.pass_context
def waydroid_create(ctx: click.Context, name: str, image: str,
                    image_type: str, arch: str, gpu: bool,
                    disk_size: str, project: str) -> None:
    """Provision an Incus container with Waydroid pre-installed."""
    ctx.obj["client"].post("/api/v1/provisioning/waydroid", json={
        "name": name, "image": image, "image_type": image_type,
        "arch": arch, "gpu": gpu, "disk_size": disk_size, "project": project,
    })


@waydroid.group("extensions")
def waydroid_extensions() -> None:
    """Manage Waydroid extensions."""


@waydroid_extensions.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def waydroid_ext_list(ctx: click.Context, name: str, project: str) -> None:
    """List installed extensions."""
    ctx.obj["client"].get(f"/api/v1/provisioning/waydroid/{name}/extensions",
                          params={"project": project})


@waydroid_extensions.command("install")
@click.argument("name")
@click.argument("extension",
                type=click.Choice(["gapps", "microg", "magisk",
                                   "libhoudini", "libndk", "widevine", "keymapper"]))
@click.option("--project", default="")
@click.pass_context
def waydroid_ext_install(ctx: click.Context, name: str, extension: str,
                          project: str) -> None:
    """Install a Waydroid extension."""
    ctx.obj["client"].post(f"/api/v1/provisioning/waydroid/{name}/extensions",
                           json={"extension": extension, "project": project})


@waydroid_extensions.command("remove")
@click.argument("name")
@click.argument("extension")
@click.option("--project", default="")
@click.pass_context
def waydroid_ext_remove(ctx: click.Context, name: str, extension: str,
                         project: str) -> None:
    """Remove a Waydroid extension."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/waydroid/{name}/extensions/{extension}",
        params={"project": project})


@waydroid.group("backup")
def waydroid_backup() -> None:
    """Backup and restore Waydroid data."""


@waydroid_backup.command("list")
@click.argument("name")
@click.option("--project", default="")
@click.pass_context
def waydroid_backup_list(ctx: click.Context, name: str, project: str) -> None:
    """List backups inside the container."""
    ctx.obj["client"].get(f"/api/v1/provisioning/waydroid/{name}/backups",
                          params={"project": project})


@waydroid_backup.command("create")
@click.argument("name")
@click.option("--dest", default="")
@click.option("--project", default="")
@click.pass_context
def waydroid_backup_create(ctx: click.Context, name: str, dest: str,
                            project: str) -> None:
    """Create a Waydroid data backup."""
    ctx.obj["client"].post(f"/api/v1/provisioning/waydroid/{name}/backups",
                           json={"dest": dest, "project": project})


@waydroid_backup.command("restore")
@click.argument("name")
@click.argument("archive")
@click.option("--project", default="")
@click.pass_context
def waydroid_backup_restore(ctx: click.Context, name: str, archive: str,
                             project: str) -> None:
    """Restore a Waydroid backup."""
    ctx.obj["client"].post(f"/api/v1/provisioning/waydroid/{name}/restore",
                           json={"archive": archive, "project": project})


@waydroid.command("cloud-sync")
@click.argument("name")
@click.option("--remote-name", required=True)
@click.option("--remote-path", required=True)
@click.option("--schedule", default="")
@click.option("--project", default="")
@click.pass_context
def waydroid_cloud_sync(ctx: click.Context, name: str, remote_name: str,
                         remote_path: str, schedule: str, project: str) -> None:
    """Configure rclone cloud sync for Waydroid backups."""
    ctx.obj["client"].put(f"/api/v1/provisioning/waydroid/{name}/cloud-sync", json={
        "remote_name": remote_name, "remote_path": remote_path,
        "schedule": schedule, "project": project,
    })


@waydroid.group("gpu")
def waydroid_gpu() -> None:
    """GPU passthrough for Waydroid containers."""


@waydroid_gpu.command("attach")
@click.argument("name")
@click.option("--dev-name", default="gpu0", show_default=True)
@click.option("--type", "gpu_type", default="physical",
              type=click.Choice(["physical", "mdev", "mig", "virtio"]))
@click.option("--pci", default="")
@click.option("--project", default="")
@click.pass_context
def waydroid_gpu_attach(ctx: click.Context, name: str, dev_name: str,
                         gpu_type: str, pci: str, project: str) -> None:
    """Attach a GPU to a Waydroid container."""
    ctx.obj["client"].post(f"/api/v1/provisioning/waydroid/{name}/gpus", json={
        "dev_name": dev_name, "gpu_type": gpu_type, "pci": pci, "project": project,
    })


@waydroid_gpu.command("detach")
@click.argument("name")
@click.argument("dev_name")
@click.option("--project", default="")
@click.pass_context
def waydroid_gpu_detach(ctx: click.Context, name: str, dev_name: str,
                         project: str) -> None:
    """Detach a GPU from a Waydroid container."""
    ctx.obj["client"].delete(
        f"/api/v1/provisioning/waydroid/{name}/gpus/{dev_name}",
        params={"project": project})


@waydroid.group("fleet")
def waydroid_fleet() -> None:
    """Bulk operations on Waydroid containers."""


@waydroid_fleet.command("list")
@click.option("--project", default="")
@click.option("--status", default="")
@click.pass_context
def waydroid_fleet_list(ctx: click.Context, project: str, status: str) -> None:
    """List Waydroid containers."""
    ctx.obj["client"].get("/api/v1/provisioning/waydroid/fleet",
                          params={"project": project, "status": status})


@waydroid.command("publish")
@click.argument("name")
@click.option("--alias", default="")
@click.option("--description", default="")
@click.option("--public/--no-public", default=False)
@click.option("--project", default="")
@click.pass_context
def waydroid_publish(ctx: click.Context, name: str, alias: str,
                      description: str, public: bool, project: str) -> None:
    """Publish a Waydroid container as a reusable Incus image."""
    ctx.obj["client"].post("/api/v1/provisioning/waydroid/publish", json={
        "name": name, "alias": alias, "description": description,
        "public": public, "project": project,
    })
