import json

from bpm_runtime.records import WorldModelRecord
from bpm_runtime.world_model import create_initial_world_model


def test_create_initial_world_model_returns_world_model_record():
    record = create_initial_world_model()

    assert isinstance(record, WorldModelRecord)
    assert record.record_type == "WorldModelRecord"


def test_initial_world_model_serializes_to_dict_and_json():
    record = create_initial_world_model()

    payload = record.to_dict()
    json_payload = json.loads(record.to_json())

    assert payload["record_type"] == "WorldModelRecord"
    assert json_payload["created_by"] == "bpm_runtime.world_model"


def test_initial_world_model_names_project_correctly():
    record = create_initial_world_model()

    assert record.project_name == "Bounded Predictive Machine"


def test_initial_world_model_marks_v0_1_v0_2_as_learning_spikes():
    record = create_initial_world_model()

    assert (
        "old_v0_1_v0_2_status: learning_spikes_not_foundation"
        in record.known_constraints
    )


def test_initial_world_model_records_architecture_commitment_and_next_stage():
    record = create_initial_world_model()

    assert record.current_phase == "world_model_first_restart"
    assert (
        "architecture_commitment: model_first_prediction_before_signal"
        in record.known_constraints
    )
    assert record.active_task == "corrected_runtime_build"
    assert "corrected_runtime_build" in record.expected_next_signal_features


def test_initial_world_model_preserves_source_refs_and_uncertainty():
    record = create_initial_world_model(source_refs=["prior-doc-5"])

    assert record.source_refs == ["prior-doc-5"]
    assert "prediction behavior not implemented yet" in record.uncertainty
    assert record.to_dict()["source_refs"] == ["prior-doc-5"]
