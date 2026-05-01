import json

from bpm_runtime.body import create_initial_body_state
from bpm_runtime.records import BodyStateRecord


def test_create_initial_body_state_returns_body_state_record():
    record = create_initial_body_state(project_root="C:/project")

    assert isinstance(record, BodyStateRecord)
    assert record.record_type == "BodyStateRecord"


def test_initial_body_state_serializes_to_dict_and_json():
    record = create_initial_body_state(project_root="C:/project")

    payload = record.to_dict()
    json_payload = json.loads(record.to_json())

    assert payload["record_type"] == "BodyStateRecord"
    assert json_payload["runtime_name"] == "bpm_runtime"


def test_initial_body_state_allows_only_safe_first_signal_sources():
    record = create_initial_body_state()

    assert "manual_text" in record.allowed_signal_sources
    assert "system_status" in record.allowed_signal_sources


def test_initial_body_state_does_not_allow_file_mutation_by_default():
    record = create_initial_body_state()

    assert "file_mutation" not in record.allowed_actions
    assert "write_file" not in record.allowed_actions
    assert "Source Documents/" in record.read_only_boundaries
    assert "file mutation is not admitted" in record.uncertainty


def test_initial_body_state_preserves_source_refs_and_uncertainty():
    record = create_initial_body_state(source_refs=["config-1"])

    assert record.source_refs == ["config-1"]
    assert "broad sensors are not enabled" in record.uncertainty
    assert record.to_dict()["source_refs"] == ["config-1"]
