"""Agent that scores conditions based on symptoms."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

from ..config import AgentConfig
from ..knowledge_base import Condition
from .base import AgentResult


@dataclass
class SymptomCheckerInput:
    symptoms: list[str]
    risk_factors: list[str]


@dataclass
class ConditionScore:
    condition: str
    score: float
    matched_symptoms: list[str]
    triggered_risk_factors: list[str]


class SymptomCheckerAgent:
    """Scores conditions using weighted matching."""

    def __init__(self, config: AgentConfig):
        self._config = config

    def run(self, conditions: Iterable[Condition], payload: SymptomCheckerInput) -> AgentResult:
        scores: list[ConditionScore] = []
        for condition in conditions:
            symptom_score = sum(
                self._config.symptom_weight * weight
                for symptom, weight in condition.symptoms.items()
                if symptom in payload.symptoms
            )
            risk_score = sum(
                self._config.risk_factor_weight * weight
                for factor, weight in condition.risk_modifiers.items()
                if factor in payload.risk_factors
            )
            total_score = min(1.0, symptom_score + risk_score)
            matched_symptoms = [s for s in condition.symptoms if s in payload.symptoms]
            triggered_risk_factors = [r for r in condition.risk_modifiers if r in payload.risk_factors]
            scores.append(
                ConditionScore(
                    condition=condition.name,
                    score=total_score,
                    matched_symptoms=matched_symptoms,
                    triggered_risk_factors=triggered_risk_factors,
                )
            )
        scores.sort(key=lambda item: item.score, reverse=True)
        summary_lines = [
            f"{entry.condition}: score={entry.score:.2f}"
            for entry in scores
        ]
        return AgentResult(
            summary="\n".join(["Condition scoring results:"] + summary_lines),
            details={
                "scores": [asdict(entry) for entry in scores],
            },
        )


__all__ = [
    "SymptomCheckerAgent",
    "SymptomCheckerInput",
    "ConditionScore",
]
