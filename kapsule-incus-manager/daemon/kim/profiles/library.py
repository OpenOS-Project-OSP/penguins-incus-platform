"""Bundled Incus profile preset library.

Presets are loaded from the profiles/ directory at the repo root.
Each YAML file in a category subdirectory becomes a preset.
"""

from __future__ import annotations

import pathlib
from typing import Any

import yaml

_PROFILES_DIR = pathlib.Path(__file__).parents[3] / "profiles"

# Inline fallback presets — used when the profiles/ directory is not present
_BUILTIN_PRESETS: list[dict[str, Any]] = [
    {
        "name": "gpu-passthrough",
        "description": "Pass through all host GPUs to the container",
        "category": "gpu",
        "profile": {
            "name": "gpu-passthrough",
            "description": "GPU passthrough",
            "config": {"security.privileged": "true"},
            "devices": {
                "gpu": {"type": "gpu", "gid": "44"}
            },
        },
    },
    {
        "name": "audio",
        "description": "PipeWire/PulseAudio socket sharing",
        "category": "audio",
        "profile": {
            "name": "audio",
            "description": "Audio via PipeWire socket",
            "config": {},
            "devices": {
                "pipewire": {
                    "type": "disk",
                    "source": "${XDG_RUNTIME_DIR}/pipewire-0",
                    "path": "/run/user/1000/pipewire-0",
                }
            },
        },
    },
    {
        "name": "x11-display",
        "description": "X11 display socket sharing",
        "category": "display",
        "profile": {
            "name": "x11-display",
            "description": "X11 display",
            "config": {},
            "devices": {
                "x11": {
                    "type": "disk",
                    "source": "/tmp/.X11-unix",
                    "path": "/tmp/.X11-unix",
                }
            },
        },
    },
    {
        "name": "wayland-display",
        "description": "Wayland compositor socket sharing",
        "category": "display",
        "profile": {
            "name": "wayland-display",
            "description": "Wayland display",
            "config": {},
            "devices": {
                "wayland": {
                    "type": "disk",
                    "source": "${XDG_RUNTIME_DIR}/wayland-0",
                    "path": "/run/user/1000/wayland-0",
                }
            },
        },
    },
    {
        "name": "nesting",
        "description": "Enable nested containerisation (Docker/Podman inside container)",
        "category": "nesting",
        "profile": {
            "name": "nesting",
            "description": "Nested containers",
            "config": {
                "security.nesting": "true",
                "linux.kernel_modules": "overlay",
            },
            "devices": {},
        },
    },
    {
        "name": "rocm",
        "description": "AMD ROCm GPU compute passthrough",
        "category": "rocm",
        "profile": {
            "name": "rocm",
            "description": "ROCm compute",
            "config": {"security.privileged": "true"},
            "devices": {
                "amdgpu": {"type": "gpu", "gid": "44"},
                "kfd": {"type": "unix-char", "source": "/dev/kfd"},
            },
        },
    },
]


def list_presets() -> list[dict[str, Any]]:
    """Return all available profile presets."""
    if not _PROFILES_DIR.exists():
        return _BUILTIN_PRESETS

    presets: list[dict[str, Any]] = []
    for category_dir in sorted(_PROFILES_DIR.iterdir()):
        if not category_dir.is_dir():
            continue
        category = category_dir.name
        for yaml_file in sorted(category_dir.glob("*.yaml")):
            try:
                data = yaml.safe_load(yaml_file.read_text())
                # Ensure the profile dict always has a 'name' field so
                # consumers can use it without checking for its presence.
                if "name" not in data:
                    data["name"] = yaml_file.stem
                presets.append({
                    "name": yaml_file.stem,
                    "description": data.get("description", ""),
                    "category": category,
                    "profile": data,
                })
            except Exception:
                continue

    return presets or _BUILTIN_PRESETS
