# AGENTS.md

## Project setup

Use the local project virtual environment.

Run Python commands with:

.\.venv\Scripts\python.exe

Run tests with:

.\.venv\Scripts\python.exe -m pytest

Do not install packages unless explicitly asked.
Do not request network access for normal coding or test runs.

## Project constraints

This repository is the corrected world-model-first restart of the Bounded Predictive Machine.

The architecture must preserve this order:

BodyStateRecord
PriorModelRecord
WorldModelRecord
→ PredictionRecord
→ SignalSourceRecord
→ SignalRecord
→ PredictionErrorRecord
→ EvidenceRecord
→ ModelUpdateRecord or NoUpdateRecord
→ ActionProposalRecord or NoActionRecord
→ SafetyCheckRecord
→ OutcomeRecord
→ MemoryTraceRecord
→ LoopRecord

Do not drift into:
- LLM integration
- agent frameworks
- CLI polish
- memory retrieval
- autonomous tool use
- network access
- filesystem mutation outside the repo

Prefer small, test-first implementation chunks.
