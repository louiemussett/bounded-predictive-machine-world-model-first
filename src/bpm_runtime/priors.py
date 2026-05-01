"""Builders for the structural prior model layer."""

from __future__ import annotations

from bpm_runtime.records import PriorModelRecord


def create_initial_prior_model(
    source_refs: list[str] | None = None,
) -> PriorModelRecord:
    """Create the initial priors that protect the corrected architecture."""
    return PriorModelRecord(
        created_by="bpm_runtime.priors",
        prediction_priors=[
            "prediction must come before signal interpretation",
            "prediction must be generated from body state, priors, and world model",
            "manual text is only one signal source",
        ],
        evidence_priors=[
            "signals are not automatically truth",
            "ambiguous signals should not update the world model",
            "weak evidence should produce no-update",
        ],
        safety_priors=[
            "unsafe or unclear action should produce no-action",
            "Source Documents/ is read-only unless explicitly allowed",
            "sensitive sensors are disabled until explicitly admitted",
        ],
        action_priors=[
            "no-action is valid under uncertainty",
            "action requires an expected observable effect",
        ],
        memory_priors=[
            "memory should preserve source references",
            "memory retrieval is context, not truth",
        ],
        source_refs=list(source_refs or []),
        uncertainty=[
            "priors are initial structural assumptions",
        ],
    )
