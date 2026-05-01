import json

from bpm_runtime.records import (
    ActionProposalRecord,
    BaseRecord,
    BodyStateRecord,
    EvidenceRecord,
    LoopRecord,
    MemoryTraceRecord,
    ModelUpdateRecord,
    NoActionRecord,
    NoUpdateRecord,
    OutcomeRecord,
    PredictionErrorRecord,
    PredictionRecord,
    PriorModelRecord,
    SafetyCheckRecord,
    SignalRecord,
    SignalSourceRecord,
    WorldModelRecord,
)


def test_base_record_serializes_to_dict():
    record = BaseRecord(
        id="record-1",
        created_at="2026-05-01T00:00:00+00:00",
        created_by="tests",
        loop_id="loop-1",
        status="created",
        source_refs=["source-1"],
        uncertainty=["still checking"],
    )

    assert record.to_dict() == {
        "id": "record-1",
        "record_type": "BaseRecord",
        "created_at": "2026-05-01T00:00:00+00:00",
        "created_by": "tests",
        "loop_id": "loop-1",
        "status": "created",
        "source_refs": ["source-1"],
        "uncertainty": ["still checking"],
    }


def test_base_record_serializes_to_json():
    record = BaseRecord(id="record-1", created_at="2026-05-01T00:00:00+00:00")

    payload = json.loads(record.to_json())

    assert payload["id"] == "record-1"
    assert payload["record_type"] == "BaseRecord"


def test_subclasses_have_correct_record_type():
    record_classes = [
        BodyStateRecord,
        PriorModelRecord,
        WorldModelRecord,
        PredictionRecord,
        SignalSourceRecord,
        SignalRecord,
        PredictionErrorRecord,
        EvidenceRecord,
        ModelUpdateRecord,
        NoUpdateRecord,
        ActionProposalRecord,
        NoActionRecord,
        SafetyCheckRecord,
        OutcomeRecord,
        MemoryTraceRecord,
        LoopRecord,
    ]

    for record_class in record_classes:
        record = record_class()

        assert record.record_type == record_class.__name__
        assert record.to_dict()["record_type"] == record_class.__name__


def test_source_refs_are_preserved():
    record = PredictionRecord(source_refs=["body-1", "prior-1", "world-1"])

    assert record.source_refs == ["body-1", "prior-1", "world-1"]
    assert record.to_dict()["source_refs"] == ["body-1", "prior-1", "world-1"]


def test_uncertainty_is_preserved():
    record = SignalRecord(uncertainty=["source reliability unknown"])

    assert record.uncertainty == ["source reliability unknown"]
    assert record.to_dict()["uncertainty"] == ["source reliability unknown"]


def test_records_are_json_serializable():
    records = [
        BaseRecord(),
        BodyStateRecord(allowed_signal_sources=["manual_text"]),
        PriorModelRecord(prediction_priors=["predict before signal"]),
        WorldModelRecord(expected_next_signal_features=["clear_instruction"]),
        PredictionRecord(expected_features=["clear_instruction"]),
        SignalSourceRecord(source_kind="manual_text", enabled=True),
        SignalRecord(payload={"text": "hello"}, observed_features=["manual_text"]),
        PredictionErrorRecord(comparison_result="match"),
        EvidenceRecord(quality_label="high", update_allowed=True),
        ModelUpdateRecord(prior_value={"phase": "old"}, posterior_value={"phase": "new"}),
        NoUpdateRecord(blocked_update_targets=["active_task"]),
        ActionProposalRecord(expected_effect="observable state change"),
        NoActionRecord(reason="unclear target"),
        SafetyCheckRecord(allowed=True),
        OutcomeRecord(success=True),
        MemoryTraceRecord(remaining_uncertainty=["none"]),
        LoopRecord(record_types=["BodyStateRecord"]),
    ]

    for record in records:
        json.dumps(record.to_dict())
        json.loads(record.to_json())


def test_loop_record_preserves_corrected_record_type_order():
    corrected_order = [
        "BodyStateRecord",
        "PriorModelRecord",
        "WorldModelRecord",
        "PredictionRecord",
        "SignalSourceRecord",
        "SignalRecord",
        "PredictionErrorRecord",
        "EvidenceRecord",
        "ModelUpdateRecord",
        "ActionProposalRecord",
        "SafetyCheckRecord",
        "OutcomeRecord",
        "MemoryTraceRecord",
    ]
    loop = LoopRecord(
        ordered_record_ids=[
            "body-1",
            "prior-1",
            "world-1",
            "prediction-1",
            "signal-source-1",
            "signal-1",
            "prediction-error-1",
            "evidence-1",
            "model-update-1",
            "action-1",
            "safety-1",
            "outcome-1",
            "memory-1",
        ],
        record_types=corrected_order,
    )

    assert loop.record_types == corrected_order
    assert loop.to_dict()["ordered_record_ids"] == [
        "body-1",
        "prior-1",
        "world-1",
        "prediction-1",
        "signal-source-1",
        "signal-1",
        "prediction-error-1",
        "evidence-1",
        "model-update-1",
        "action-1",
        "safety-1",
        "outcome-1",
        "memory-1",
    ]
    assert loop.record_types.index("PredictionRecord") < loop.record_types.index(
        "SignalRecord"
    )
    assert loop.record_types.index("SignalRecord") < loop.record_types.index(
        "PredictionErrorRecord"
    )
    assert loop.record_types.index("EvidenceRecord") < loop.record_types.index(
        "ModelUpdateRecord"
    )
    assert loop.record_types.index("ActionProposalRecord") < loop.record_types.index(
        "SafetyCheckRecord"
    )
    assert loop.record_types.index("SafetyCheckRecord") < loop.record_types.index(
        "OutcomeRecord"
    )


def test_loop_record_can_preserve_no_update_and_no_action_order():
    corrected_order = [
        "BodyStateRecord",
        "PriorModelRecord",
        "WorldModelRecord",
        "PredictionRecord",
        "SignalSourceRecord",
        "SignalRecord",
        "PredictionErrorRecord",
        "EvidenceRecord",
        "NoUpdateRecord",
        "NoActionRecord",
        "SafetyCheckRecord",
        "OutcomeRecord",
        "MemoryTraceRecord",
    ]

    loop = LoopRecord(record_types=corrected_order)

    assert loop.record_types == corrected_order
    assert loop.record_types.index("EvidenceRecord") < loop.record_types.index(
        "NoUpdateRecord"
    )
    assert loop.record_types.index("NoActionRecord") < loop.record_types.index(
        "SafetyCheckRecord"
    )
