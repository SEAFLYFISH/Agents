"""Orchestrates the full workflow of the medical test agents."""

from __future__ import annotations

from dataclasses import dataclass

from .agents.diagnostic_recommender import DiagnosticTestRecommenderAgent
from .agents.symptom_checker import ConditionScore, SymptomCheckerAgent, SymptomCheckerInput
from .config import PipelineConfig
from .knowledge_base import MedicalKnowledgeBase


@dataclass
class PatientProfile:
    age: int
    sex: str
    symptoms: list[str]
    risk_factors: list[str]
    flags: dict[str, str]


class MedicalTestPipeline:
    """Coordinates the different agents to produce a report."""

    def __init__(self, config: PipelineConfig | None = None):
        self._config = config or PipelineConfig.load_default()
        self._knowledge_base = MedicalKnowledgeBase.load(self._config.knowledge_base_path)
        self._symptom_agent = SymptomCheckerAgent(self._config.agent)
        self._test_agent = DiagnosticTestRecommenderAgent(self._config.agent)

    def run(self, profile: PatientProfile) -> str:
        """Run the full pipeline and return a textual report."""

        conditions = list(self._knowledge_base.iter_conditions())
        symptom_result = self._symptom_agent.run(
            conditions,
            SymptomCheckerInput(
                symptoms=profile.symptoms,
                risk_factors=profile.risk_factors,
            ),
        )

        scores = [
            ConditionScore(**score) if isinstance(score, dict) else score
            for score in symptom_result.details["scores"]
        ]

        test_result = self._test_agent.run(
            conditions,
            scores,
            profile.flags,
        )

        summary_lines = [
            "Diagnostic Summary",
            "------------------",
            f"Symptoms: {', '.join(profile.symptoms) or 'None'}",
            f"Risk Factors: {', '.join(profile.risk_factors) or 'None'}",
            "",
        ]

        report_lines = [
            "Medical Test Recommendation Report",
            "=" * 40,
            "Patient Profile:",
            f"- Age: {profile.age}",
            f"- Sex: {profile.sex}",
            f"- Symptoms: {', '.join(profile.symptoms) or 'None'}",
            f"- Risk Factors: {', '.join(profile.risk_factors) or 'None'}",
            "",
            *summary_lines,
            symptom_result.summary,
            "",
            test_result.summary,
        ]
        return "\n".join(report_lines)


__all__ = ["MedicalTestPipeline", "PatientProfile"]
