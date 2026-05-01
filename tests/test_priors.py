import json

from bpm_runtime.priors import create_initial_prior_model
from bpm_runtime.records import PriorModelRecord


def test_create_initial_prior_model_returns_prior_model_record():
    record = create_initial_prior_model()

    assert isinstance(record, PriorModelRecord)
    assert record.record_type == "PriorModelRecord"


def test_initial_prior_model_serializes_to_dict_and_json():
    record = create_initial_prior_model()

    payload = record.to_dict()
    json_payload = json.loads(record.to_json())

    assert payload["record_type"] == "PriorModelRecord"
    assert json_payload["created_by"] == "bpm_runtime.priors"


def test_initial_prior_model_treats_signals_as_not_automatically_truth():
    record = create_initial_prior_model()

    assert "signals are not automatically truth" in record.evidence_priors


def test_initial_prior_model_places_prediction_before_signal_interpretation():
    record = create_initial_prior_model()

    assert (
        "prediction must come before signal interpretation"
        in record.prediction_priors
    )


def test_initial_prior_model_preserves_source_refs_and_uncertainty():
    record = create_initial_prior_model(source_refs=["doc-1", "doc-2"])

    assert record.source_refs == ["doc-1", "doc-2"]
    assert "priors are initial structural assumptions" in record.uncertainty
    assert record.to_dict()["source_refs"] == ["doc-1", "doc-2"]
