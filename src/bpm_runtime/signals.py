"""Bounded signal source and signal capture helpers."""

from __future__ import annotations

from bpm_runtime.records import BodyStateRecord, PredictionRecord, SignalRecord, SignalSourceRecord


def create_manual_text_signal_source(
    body_state: BodyStateRecord,
) -> SignalSourceRecord:
    """Represent manual text as one bounded source admitted by body state."""
    manual_text_allowed = "manual_text" in body_state.allowed_signal_sources

    if manual_text_allowed:
        status = "available"
        permission_status = "allowed"
        enabled = True
        uncertainty = [
            "manual text is one bounded signal source, not the root of cognition",
            "manual text may be incomplete or ambiguous",
        ]
    else:
        status = "blocked"
        permission_status = "not_admitted_by_body_state"
        enabled = False
        uncertainty = [
            "manual_text is not admitted by the current body state",
        ]

    return SignalSourceRecord(
        created_by="bpm_runtime.signals",
        status=status,
        source_refs=[body_state.id],
        uncertainty=uncertainty,
        source_name="ManualTextSignalSource",
        source_kind="manual_text",
        enabled=enabled,
        permission_status=permission_status,
        scope="explicitly provided user text only",
        read_write_mode="read_only",
        expected_signal_types=["manual_text_input"],
    )


def capture_manual_text_signal(
    signal_source: SignalSourceRecord,
    prediction: PredictionRecord,
    text: str,
) -> SignalRecord:
    """Capture manual text after prediction, without interpreting it as truth."""
    raw_text = text
    stripped_text = raw_text.strip()
    observed_features = _observed_features(stripped_text)
    uncertainty = [
        "manual text is an observation candidate, not truth",
        "signal has not been compared against prediction yet",
    ]
    if stripped_text:
        uncertainty.append("manual text may be ambiguous or incomplete")
    else:
        uncertainty.append("manual text payload is empty")

    return SignalRecord(
        created_by="bpm_runtime.signals",
        status="captured",
        source_refs=[signal_source.id, prediction.id],
        uncertainty=uncertainty,
        source_id=signal_source.id,
        source_type="manual_text",
        payload={"text": raw_text},
        payload_summary=_payload_summary(stripped_text),
        observed_features=observed_features,
        boundary_status="inside_manual_text_boundary",
        admissibility_status="admissible"
        if signal_source.enabled and signal_source.source_kind == "manual_text"
        else "inadmissible",
    )


def _observed_features(stripped_text: str) -> list[str]:
    if not stripped_text:
        return ["empty_text"]
    return ["contains_text", "possible_project_instruction"]


def _payload_summary(stripped_text: str) -> str:
    if not stripped_text:
        return "Empty manual text signal."
    return "Manual text signal captured without truth interpretation."
