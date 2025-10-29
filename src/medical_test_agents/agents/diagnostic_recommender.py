"""Agent that recommends diagnostic tests based on condition scores."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from ..config import AgentConfig
from ..knowledge_base import Condition
from .base import AgentResult
from .symptom_checker import ConditionScore


@dataclass
class TestRecommendation:
    test: str
    condition: str
    rationale: str
    contraindicated: bool
    contraindication_reason: str | None = None


class DiagnosticTestRecommenderAgent:
    """Suggest diagnostic tests based on scored conditions."""

    def __init__(self, config: AgentConfig):
        self._config = config

    def run(
        self,
        conditions: Iterable[Condition],
        scores: list[ConditionScore],
        patient_profile: dict[str, str],
    ) -> AgentResult:
        recommendations: list[TestRecommendation] = []
        condition_map = {condition.name: condition for condition in conditions}
        for score in scores:
            if score.score < self._config.test_threshold:
                continue
            condition = condition_map.get(score.condition)
            if not condition:
                continue
            for test in condition.recommended_tests:
                contraindication_reason = None
                contraindicated = False
                for factor, reason in condition.contraindications.items():
                    if patient_profile.get(factor) == "true":
                        contraindication_reason = reason
                        contraindicated = True
                        break
                rationale = (
                    f"Condition '{condition.name}' scored {score.score:.2f} based on"
                    f" symptoms {', '.join(score.matched_symptoms) or 'none'}"
                )
                recommendations.append(
                    TestRecommendation(
                        test=test,
                        condition=condition.name,
                        rationale=rationale,
                        contraindicated=contraindicated,
                        contraindication_reason=contraindication_reason,
                    )
                )
        summary_lines = [
            f"{item.test} (for {item.condition}) - {'contraindicated' if item.contraindicated else 'recommended'}"
            for item in recommendations
        ] or ["No tests met the recommendation threshold."]
        return AgentResult(
            summary="\n".join(["Test recommendations:"] + summary_lines),
            details={
                "recommendations": [item.__dict__ for item in recommendations],
            },
        )


__all__ = ["DiagnosticTestRecommenderAgent", "TestRecommendation"]
