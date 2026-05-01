"""Minimal record models for the world-model-first BPM restart."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
import json
from typing import Any
from uuid import uuid4


def _new_id() -> str:
    return str(uuid4())


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _json_safe(value: Any) -> Any:
    if isinstance(value, dict):
        return {str(key): _json_safe(item) for key, item in value.items()}
    if isinstance(value, (list, tuple, set)):
        return [_json_safe(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


@dataclass
class BaseRecord:
    id: str = field(default_factory=_new_id)
    record_type: str = field(init=False)
    created_at: str = field(default_factory=_utc_now)
    created_by: str = "bpm_runtime.records"
    loop_id: str | None = None
    status: str = "created"
    source_refs: list[str] = field(default_factory=list)
    uncertainty: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        self.record_type = self.__class__.__name__

    def to_dict(self) -> dict[str, Any]:
        return _json_safe(asdict(self))

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


@dataclass
class BodyStateRecord(BaseRecord):
    runtime_name: str | None = None
    execution_mode: str | None = None
    project_root: str | None = None
    allowed_signal_sources: list[str] = field(default_factory=list)
    allowed_actions: list[str] = field(default_factory=list)
    read_only_boundaries: list[str] = field(default_factory=list)
    safety_mode: str | None = None


@dataclass
class PriorModelRecord(BaseRecord):
    prediction_priors: list[str] = field(default_factory=list)
    evidence_priors: list[str] = field(default_factory=list)
    safety_priors: list[str] = field(default_factory=list)
    action_priors: list[str] = field(default_factory=list)
    memory_priors: list[str] = field(default_factory=list)


@dataclass
class WorldModelRecord(BaseRecord):
    project_name: str | None = None
    current_phase: str | None = None
    active_task: str | None = None
    known_constraints: list[str] = field(default_factory=list)
    available_signal_sources: list[str] = field(default_factory=list)
    expected_next_signal_features: list[str] = field(default_factory=list)
    confidence: str | None = None


@dataclass
class PredictionRecord(BaseRecord):
    prediction_target: str | None = None
    expected_source: str | None = None
    expected_features: list[str] = field(default_factory=list)
    match_conditions: list[str] = field(default_factory=list)
    mismatch_conditions: list[str] = field(default_factory=list)
    confidence: str | None = None
    prediction_basis: list[str] = field(default_factory=list)


@dataclass
class SignalSourceRecord(BaseRecord):
    source_name: str | None = None
    source_kind: str | None = None
    enabled: bool = False
    permission_status: str | None = None
    scope: str | None = None
    read_write_mode: str | None = None
    expected_signal_types: list[str] = field(default_factory=list)


@dataclass
class SignalRecord(BaseRecord):
    source_id: str | None = None
    source_type: str | None = None
    payload: Any = None
    payload_summary: str | None = None
    observed_features: list[str] = field(default_factory=list)
    boundary_status: str | None = None
    admissibility_status: str | None = None


@dataclass
class PredictionErrorRecord(BaseRecord):
    prediction_ref: str | None = None
    signal_ref: str | None = None
    comparison_result: str | None = None
    matched_features: list[str] = field(default_factory=list)
    missing_features: list[str] = field(default_factory=list)
    unexpected_features: list[str] = field(default_factory=list)
    mismatched_features: list[str] = field(default_factory=list)
    error_summary: str | None = None


@dataclass
class EvidenceRecord(BaseRecord):
    prediction_error_ref: str | None = None
    quality_label: str | None = None
    reasons: list[str] = field(default_factory=list)
    recommended_result: str | None = None
    update_allowed: bool = False
    action_allowed: bool = False


@dataclass
class ModelUpdateRecord(BaseRecord):
    model_ref: str | None = None
    update_target: str | None = None
    prior_value: Any = None
    posterior_value: Any = None
    reason: str | None = None
    evidence_ref: str | None = None


@dataclass
class NoUpdateRecord(BaseRecord):
    model_ref: str | None = None
    reason: str | None = None
    evidence_ref: str | None = None
    blocked_update_targets: list[str] = field(default_factory=list)
    required_evidence_for_update: list[str] = field(default_factory=list)


@dataclass
class ActionProposalRecord(BaseRecord):
    action_name: str | None = None
    action_type: str | None = None
    action_target: str | None = None
    expected_effect: str | None = None
    reason: str | None = None
    risk_level: str | None = None
    permission_required: str | None = None


@dataclass
class NoActionRecord(BaseRecord):
    reason: str | None = None
    blocked_action_names: list[str] = field(default_factory=list)
    required_condition_for_action: list[str] = field(default_factory=list)


@dataclass
class SafetyCheckRecord(BaseRecord):
    action_ref: str | None = None
    allowed: bool = False
    reason: str | None = None
    boundary_status: str | None = None
    permission_status: str | None = None


@dataclass
class OutcomeRecord(BaseRecord):
    action_ref: str | None = None
    no_action_ref: str | None = None
    safety_ref: str | None = None
    expected_effect: str | None = None
    observed_effect: str | None = None
    success: bool = False
    unresolved_questions: list[str] = field(default_factory=list)


@dataclass
class MemoryTraceRecord(BaseRecord):
    referenced_record_ids: list[str] = field(default_factory=list)
    referenced_record_types: list[str] = field(default_factory=list)
    reconstruction_summary: str | None = None
    remaining_uncertainty: list[str] = field(default_factory=list)


@dataclass
class LoopRecord(BaseRecord):
    ordered_record_ids: list[str] = field(default_factory=list)
    record_types: list[str] = field(default_factory=list)
