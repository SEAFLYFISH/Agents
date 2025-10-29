"""Configuration utilities for the medical test agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class AgentConfig:
    """Configuration for agent thresholds and weights."""

    symptom_weight: float = 1.0
    risk_factor_weight: float = 1.5
    test_threshold: float = 0.4


@dataclass
class PipelineConfig:
    """Top-level configuration for the pipeline."""

    knowledge_base_path: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2] / "data" / "medical_knowledge.json")
    agent: AgentConfig = field(default_factory=AgentConfig)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "PipelineConfig":
        """Create a configuration instance from a plain dictionary."""

        knowledge_base_path = data.get("knowledge_base_path")
        if knowledge_base_path is not None:
            path = Path(knowledge_base_path)
        else:
            path = Path(__file__).resolve().parents[2] / "data" / "medical_knowledge.json"

        agent_data = data.get("agent", {})
        agent_config = AgentConfig(
            symptom_weight=float(agent_data.get("symptom_weight", AgentConfig.symptom_weight)),
            risk_factor_weight=float(agent_data.get("risk_factor_weight", AgentConfig.risk_factor_weight)),
            test_threshold=float(agent_data.get("test_threshold", AgentConfig.test_threshold)),
        )
        return cls(knowledge_base_path=path, agent=agent_config)

    @classmethod
    def load_default(cls) -> "PipelineConfig":
        """Load the default configuration bundled with the package."""

        return cls()


DEFAULT_CONFIG = PipelineConfig.load_default()

__all__ = ["AgentConfig", "PipelineConfig", "DEFAULT_CONFIG"]
