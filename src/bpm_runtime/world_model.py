"""Builders for the initial world-model layer."""

from __future__ import annotations

from bpm_runtime.records import WorldModelRecord


def create_initial_world_model(
    source_refs: list[str] | None = None,
) -> WorldModelRecord:
    """Create the initial project model before any prediction is generated."""
    return WorldModelRecord(
        created_by="bpm_runtime.world_model",
        project_name="Bounded Predictive Machine",
        current_phase="world_model_first_restart",
        active_task="corrected_runtime_build",
        known_constraints=[
            "old_v0_1_v0_2_status: learning_spikes_not_foundation",
            "architecture_commitment: model_first_prediction_before_signal",
            "manual_text_is_one_signal_source_not_root",
            "do_not_add_llm_integration",
            "do_not_add_cli_commands_yet",
        ],
        available_signal_sources=["manual_text", "system_status"],
        expected_next_signal_features=[
            "corrected_runtime_build",
            "pre_prediction_state_layer",
            "body_priors_world_model_before_prediction",
        ],
        confidence="medium",
        source_refs=list(source_refs or []),
        uncertainty=[
            "prediction behavior not implemented yet",
        ],
    )
