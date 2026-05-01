"""Builders for the runtime body-state layer."""

from __future__ import annotations

from pathlib import Path

from bpm_runtime.records import BodyStateRecord


def create_initial_body_state(
    project_root: str | None = None,
    source_refs: list[str] | None = None,
) -> BodyStateRecord:
    """Create the conservative starting body state before prediction exists."""
    return BodyStateRecord(
        created_by="bpm_runtime.body",
        runtime_name="bpm_runtime",
        execution_mode="local_prototype",
        project_root=project_root or str(Path.cwd()),
        allowed_signal_sources=["manual_text", "system_status"],
        allowed_actions=["no_action", "propose_action"],
        read_only_boundaries=["Source Documents/"],
        safety_mode="conservative",
        source_refs=list(source_refs or []),
        uncertainty=[
            "broad sensors are not enabled",
            "file mutation is not admitted",
        ],
    )
