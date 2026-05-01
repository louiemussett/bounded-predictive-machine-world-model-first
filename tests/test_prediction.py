import inspect
import json

from bpm_runtime.body import create_initial_body_state
from bpm_runtime.prediction import create_prediction_from_state
from bpm_runtime.priors import create_initial_prior_model
from bpm_runtime.records import LoopRecord, PredictionRecord, SignalRecord
from bpm_runtime.world_model import create_initial_world_model


def _initial_state_records():
    return (
        create_initial_body_state(project_root="C:/project"),
        create_initial_prior_model(),
        create_initial_world_model(),
    )


def test_create_prediction_from_state_returns_prediction_record():
    body_state, prior_model, world_model = _initial_state_records()

    prediction = create_prediction_from_state(body_state, prior_model, world_model)

    assert isinstance(prediction, PredictionRecord)
    assert prediction.record_type == "PredictionRecord"


def test_prediction_source_refs_include_pre_prediction_state_records():
    body_state, prior_model, world_model = _initial_state_records()

    prediction = create_prediction_from_state(body_state, prior_model, world_model)

    assert prediction.source_refs == [body_state.id, prior_model.id, world_model.id]


def test_prediction_serializes_to_dict_and_json():
    body_state, prior_model, world_model = _initial_state_records()

    prediction = create_prediction_from_state(body_state, prior_model, world_model)
    payload = prediction.to_dict()
    json_payload = json.loads(prediction.to_json())

    assert payload["record_type"] == "PredictionRecord"
    assert json_payload["expected_signal_type"] == "instruction_or_project_signal"


def test_prediction_contains_structured_expectation_data():
    body_state, prior_model, world_model = _initial_state_records()

    prediction = create_prediction_from_state(body_state, prior_model, world_model)

    assert prediction.expected_source == "manual_text"
    assert prediction.expected_signal_type == "instruction_or_project_signal"
    assert "project_continuation_request" in prediction.expected_features
    assert "architecture_or_implementation_request" in prediction.expected_features
    assert prediction.match_conditions
    assert prediction.mismatch_conditions
    assert prediction.prediction_basis
    assert prediction.confidence == "medium"


def test_prediction_uncertainty_records_that_no_signal_has_been_observed():
    body_state, prior_model, world_model = _initial_state_records()

    prediction = create_prediction_from_state(body_state, prior_model, world_model)

    assert "no signal has been observed yet" in prediction.uncertainty


def test_create_prediction_from_state_does_not_require_manual_text_input():
    signature = inspect.signature(create_prediction_from_state)

    assert list(signature.parameters) == [
        "body_state",
        "prior_model",
        "world_model",
    ]

    body_state, prior_model, world_model = _initial_state_records()
    prediction = create_prediction_from_state(body_state, prior_model, world_model)

    assert prediction.expected_source == "manual_text"


def test_prediction_can_be_created_before_any_signal_record_exists():
    body_state, prior_model, world_model = _initial_state_records()

    prediction = create_prediction_from_state(body_state, prior_model, world_model)
    later_signal = SignalRecord(source_type="manual_text")
    loop = LoopRecord(
        ordered_record_ids=[
            body_state.id,
            prior_model.id,
            world_model.id,
            prediction.id,
            later_signal.id,
        ],
        record_types=[
            body_state.record_type,
            prior_model.record_type,
            world_model.record_type,
            prediction.record_type,
            later_signal.record_type,
        ],
    )

    assert loop.record_types.index("PredictionRecord") < loop.record_types.index(
        "SignalRecord"
    )
