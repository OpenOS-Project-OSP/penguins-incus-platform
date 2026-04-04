"""Resource usage polling task.

Polls Incus every 5 seconds for CPU/memory/disk stats of all running instances
and publishes ResourceUsageUpdated D-Bus signals + synthetic events to the EventBus.

CPU usage is computed as an instantaneous percentage by diffing consecutive
cumulative nanosecond counters against wall-clock elapsed time:

    cpu_fraction = Δcpu_ns / (Δwall_ns * num_cpus)

On the first sample for a given instance there is no previous reading, so
cpu_usage is reported as 0.0 and the baseline is stored for the next cycle.
"""

from __future__ import annotations

import asyncio
import logging
import time
from typing import Any

from .events import EventBus
from .incus.client import IncusClient

logger = logging.getLogger(__name__)

_POLL_INTERVAL = 5  # seconds


# ── CPU diff helpers ──────────────────────────────────────────────────────────

class _CpuSample:
    """One recorded CPU sample for a single instance."""
    __slots__ = ("cpu_ns", "wall_ns")

    def __init__(self, cpu_ns: int, wall_ns: float) -> None:
        self.cpu_ns  = cpu_ns
        self.wall_ns = wall_ns


def calc_cpu_fraction(
    prev: _CpuSample,
    curr_cpu_ns: int,
    curr_wall_ns: float,
    num_cpus: int = 1,
) -> float:
    """Return instantaneous CPU fraction (0.0-1.0) from two consecutive samples.

    Args:
        prev:         Previous sample (cpu_ns + wall_ns).
        curr_cpu_ns:  Current cumulative CPU nanoseconds from Incus state.
        curr_wall_ns: Current wall-clock time in nanoseconds (time.monotonic_ns()).
        num_cpus:     Number of logical CPUs available to the instance.

    Returns:
        CPU fraction clamped to [0.0, 1.0].  Returns 0.0 if the wall-clock
        delta is zero (e.g. two samples taken at the same instant).
    """
    delta_cpu  = max(curr_cpu_ns  - prev.cpu_ns,  0)
    delta_wall = max(curr_wall_ns - prev.wall_ns, 0.0)
    if delta_wall == 0.0 or num_cpus <= 0:
        return 0.0
    return min(delta_cpu / (delta_wall * num_cpus), 1.0)


# ── Main polling loop ─────────────────────────────────────────────────────────

async def poll_resource_usage(incus: IncusClient, bus: EventBus) -> None:
    """Run forever, emitting resource usage events every _POLL_INTERVAL seconds."""
    # Keyed by (project, name) -> _CpuSample from the previous poll cycle.
    _prev_cpu: dict[tuple[str, str], _CpuSample] = {}

    while True:
        try:
            instances = await incus.list_instances()
            now_ns = float(time.monotonic_ns())

            for inst in instances:
                if inst.get("status") != "Running":
                    continue

                name    = inst.get("name", "")
                project = inst.get("project", "default")
                state   = inst.get("state", {})

                if not state:
                    try:
                        detail = await incus.get_instance(name, project=project)
                        state  = detail.get("state", {})
                    except Exception:
                        continue

                curr_cpu_ns = _read_cpu_ns(state)
                key         = (project, name)
                prev        = _prev_cpu.get(key)

                if prev is None:
                    # First sample -- store baseline, report 0 this cycle.
                    cpu_usage = 0.0
                else:
                    cpu_usage = calc_cpu_fraction(prev, curr_cpu_ns, now_ns)

                _prev_cpu[key] = _CpuSample(curr_cpu_ns, now_ns)

                event: dict[str, Any] = {
                    "type":      "resource_usage",
                    "project":   project,
                    "timestamp": "",
                    "metadata": {
                        "name":               name,
                        "cpu_usage":          cpu_usage,
                        "memory_usage_bytes": _parse_memory(state),
                        "disk_usage_bytes":   _parse_disk(state),
                    },
                }
                await bus.publish(event)

            # Evict stale entries for instances that are no longer running.
            running_keys = {
                (inst.get("project", "default"), inst.get("name", ""))
                for inst in instances
                if inst.get("status") == "Running"
            }
            for stale in set(_prev_cpu) - running_keys:
                del _prev_cpu[stale]

        except asyncio.CancelledError:
            raise
        except Exception as exc:
            logger.debug("Resource poll error: %s", exc)

        await asyncio.sleep(_POLL_INTERVAL)


# ── State parsing helpers ─────────────────────────────────────────────────────

def _read_cpu_ns(state: dict[str, Any]) -> int:
    """Return cumulative CPU nanoseconds from an Incus instance state dict."""
    return int(state.get("cpu", {}).get("usage", 0))


def _parse_memory(state: dict[str, Any]) -> int:
    return int(state.get("memory", {}).get("usage", 0))


def _parse_disk(state: dict[str, Any]) -> int:
    disk = state.get("disk", {})
    return sum(int(dev.get("usage", 0)) for dev in disk.values())
