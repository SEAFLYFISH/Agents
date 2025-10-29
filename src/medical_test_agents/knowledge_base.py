"""Utilities for loading medical knowledge data."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Mapping


@dataclass
class Condition:
    """Representation of a medical condition."""

    name: str
    symptoms: Mapping[str, float]
    risk_modifiers: Mapping[str, float]
    recommended_tests: list[str]
    contraindications: Mapping[str, str]


@dataclass
class MedicalKnowledgeBase:
    """A collection of conditions keyed by name."""

    conditions: dict[str, Condition]

    @classmethod
    def load(cls, path: Path) -> "MedicalKnowledgeBase":
        data = json.loads(path.read_text())
        conditions: dict[str, Condition] = {}
        for entry in data.get("conditions", []):
            condition = Condition(
                name=entry["name"],
                symptoms=entry.get("symptoms", {}),
                risk_modifiers=entry.get("risk_modifiers", {}),
                recommended_tests=list(entry.get("recommended_tests", [])),
                contraindications=entry.get("contraindications", {}),
            )
            conditions[condition.name] = condition
        return cls(conditions=conditions)

    def iter_conditions(self) -> Iterable[Condition]:
        return self.conditions.values()


__all__ = ["Condition", "MedicalKnowledgeBase"]
