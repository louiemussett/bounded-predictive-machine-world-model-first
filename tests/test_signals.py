import inspect
import json

from bpm_runtime.body import create_initial_body_state
from bpm_runtime.prediction import create_prediction_from_state
from bpm_runtime.priors import create_initial_prior_model
from bpm_runtime.records import (
    EvidenceRecord,
    LoopRecord,
    ModelUpdateRecord,
    PredictionErrorRecord,
    SignalRecord,
    SignalSourceRecord,
    WorldModelRecord,
)
from bpm_runtime.signals import (
    capture_manual_text_signal,
    create_manual_text_signal_source,
)
from bpm_runtime.world_model import create_initial_world_model


def _prediction_ready_records():
    body_state = create_initial_body_state(project_root="C:/project")
    prior_model = create_initial_prior_model()
    world_model = create_initial_world_model()
    prediction = create_prediction_from_state(body_state, prior_model, world_model)
    signal_source = create_manual_text_signal_source(body_state)
    return body_state, prior_model, world_model, prediction, signal_source


def test_create_manual_text_signal_source_returns_signal_source_record():
    body_state = create_initial_body_state()

    signal_source = create_manual_text_signal_source(body_state)

    assert isinstance(signal_source, SignalSourceRecord)
    assert signal_source.record_type == "SignalSourceRecord"


def test_manual_text_source_is_allowed_when_body_state_allows_it():
    body_state = create_initial_body_state()

    signal_source = create_manual_text_signal_source(body_state)

    assert signal_source.source_kind == "manual_text"
    assert signal_source.enabled is True
    assert signal_source.status == "available"
    assert signal_source.permission_status == "allowed"
    assert signal_source.read_write_mode == "read_only"


def test_manual_text_source_refs_include_body_state_id():
    body_state = create_initial_body_state()

    signal_source = create_manual_text_signal_source(body_state)

    assert signal_source.source_refs == [body_state.id]
    assert signal_source.to_dict()["source_refs"] == [body_state.id]


def test_capture_manual_text_signal_returns_signal_record():
    _, _, _, prediction, signal_source = _prediction_ready_records()

    signal = capture_manual_text_signal(signal_source, prediction, "continue")

    assert isinstance(signal, SignalRecord)
    assert signal.record_type == "SignalRecord"


def test_signal_record_source_refs_include_source_and_prediction_ids():
    _, _, _, prediction, signal_source = _prediction_ready_records()

    signal = capture_manual_text_signal(signal_source, prediction, "continue")

    assert signal.source_refs == [signal_source.id, prediction.id]


def test_signal_record_serializes_to_dict_and_json():
    _, _, _, prediction, signal_source = _prediction_ready_records()

    signal = capture_manual_text_signal(signal_source, prediction, "continue")
    payload = signal.to_dict()
    json_payload = json.loads(signal.to_json())

    assert payload["record_type"] == "SignalRecord"
    assert json_payload["source_type"] == "manual_text"
    assert json_payload["payload"] == {"text": "continue"}


def test_empty_text_produces_empty_text_observed_feature():
    _, _, _, prediction, signal_source = _prediction_ready_records()

    signal = capture_manual_text_signal(signal_source, prediction, "   ")

    assert signal.observed_features == ["empty_text"]
    assert "manual text payload is empty" in signal.uncertainty


def test_non_empty_text_produces_contains_text_observed_feature():
    _, _, _, prediction, signal_source = _prediction_ready_records()

    signal = capture_manual_text_signal(signal_source, prediction, "build next layer")

    assert "contains_text" in signal.observed_features
    assert "possible_project_instruction" in signal.observed_features


def test_signal_capture_requires_prediction_record_argument():
    signature = inspect.signature(capture_manual_text_signal)

    assert list(signature.parameters) == ["signal_source", "prediction", "text"]


def test_signal_capture_does_not_create_downstream_records_or_update_world_model():
    _, _, world_model, prediction, signal_source = _prediction_ready_records()

    signal = capture_manual_text_signal(signal_source, prediction, "build next layer")

    assert isinstance(signal, SignalRecord)
    assert not isinstance(signal, PredictionErrorRecord)
    assert not isinstance(signal, EvidenceRecord)
    assert not isinstance(signal, ModelUpdateRecord)
    assert not isinstance(signal, WorldModelRecord)
    assert world_model.current_phase == "world_model_first_restart"
    assert signal.source_refs == [signal_source.id, prediction.id]


def test_manual_text_is_one_bounded_source_not_loop_root():
    body_state, prior_model, world_model, prediction, signal_source = (
        _prediction_ready_records()
    )
    signal = capture_manual_text_signal(signal_source, prediction, "continue")
    loop = LoopRecord(
        ordered_record_ids=[
            body_state.id,
            prior_model.id,
            world_model.id,
            prediction.id,
            signal_source.id,
            signal.id,
        ],
        record_types=[
            body_state.record_type,
            prior_model.record_type,
            world_model.record_type,
            prediction.record_type,
            signal_source.record_type,
            signal.record_type,
        ],
    )

    assert signal_source.source_kind == "manual_text"
    assert loop.record_types.index("PredictionRecord") < loop.record_types.index(
        "SignalSourceRecord"
    )
    assert loop.record_types.index("SignalSourceRecord") < loop.record_types.index(
        "SignalRecord"
    )
    assert loop.record_types[0] == "BodyStateRecord"
