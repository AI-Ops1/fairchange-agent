"""Durable JSON state for idempotent FairChange processing."""

from __future__ import annotations

import json
import os
from pathlib import Path

from .domain import WorkflowState


class JsonWorkflowStore:
    def __init__(self, path: str | Path):
        self.path = Path(path)

    def load(self) -> WorkflowState:
        if not self.path.exists():
            return WorkflowState()
        return WorkflowState.from_dict(json.loads(self.path.read_text(encoding="utf-8")))

    def save(self, state: WorkflowState) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        temporary = self.path.with_suffix(self.path.suffix + ".tmp")
        temporary.write_text(
            json.dumps(state.to_dict(), indent=2, sort_keys=True), encoding="utf-8"
        )
        os.replace(temporary, self.path)
