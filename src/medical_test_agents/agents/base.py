"""Base classes for agents."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class Agent(Protocol):
    """Protocol for simple agents."""

    def run(self, *args: Any, **kwargs: Any) -> Any:  # pragma: no cover - interface only
        ...


@dataclass
class AgentResult:
    """Result returned by agents."""

    summary: str
    details: dict[str, Any]

    def merge(self, other: "AgentResult") -> "AgentResult":
        merged_details = {**self.details, **other.details}
        return AgentResult(summary=f"{self.summary}\n{other.summary}", details=merged_details)


__all__ = ["Agent", "AgentResult"]
