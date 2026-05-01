"""Prediction builders for the world-model-first runtime."""

from __future__ import annotations

from bpm_runtime.records import (
    BodyStateRecord,
    PredictionRecord,
    PriorModelRecord,
    WorldModelRecord,
)


def create_prediction_from_state(
    body_state: BodyStateRecord,
    prior_model: PriorModelRecord,
    world_model: WorldModelRecord,
) -> PredictionRecord:
    """Create a prediction from pre-signal state records only."""
    expected_source = _select_expected_source(body_state, world_model)
    expected_features = _expected_features_from_world_model(world_model)

    return PredictionRecord(
        created_by="bpm_runtime.prediction",
        prediction_target="next_signal",
        expected_source=expected_source,
        expected_signal_type="instruction_or_project_signal",
        expected_features=expected_features,
        match_conditions=[
            f"signal source is {expected_source}",
            "signal contains a project continuation or architecture request",
            "signal is inside an admitted source boundary",
        ],
        mismatch_conditions=[
            "signal is empty",
            "signal is unrelated to the current project",
            "signal comes from a disabled or unexpected source",
            "signal asks for an unsafe or unclear action",
        ],
        confidence="medium",
        prediction_basis=[
            f"body allows signal sources: {', '.join(body_state.allowed_signal_sources)}",
            "prior requires prediction before signal interpretation",
            f"world phase is {world_model.current_phase}",
            f"world active task is {world_model.active_task}",
        ],
        source_refs=[body_state.id, prior_model.id, world_model.id],
        uncertainty=[
            "no signal has been observed yet",
            "manual text may not be the next signal",
            "world model may need revision after evidence",
        ],
    )


def _select_expected_source(
    body_state: BodyStateRecord,
    world_model: WorldModelRecord,
) -> str | None:
    if (
        "manual_text" in body_state.allowed_signal_sources
        and "manual_text" in world_model.available_signal_sources
    ):
        return "manual_text"
    if body_state.allowed_signal_sources:
        return body_state.allowed_signal_sources[0]
    return None


def _expected_features_from_world_model(
    world_model: WorldModelRecord,
) -> list[str]:
    features = [
        "project_continuation_request",
        "architecture_or_implementation_request",
    ]
    for feature in world_model.expected_next_signal_features:
        if feature not in features:
            features.append(feature)
    return features
