"""Command line interface for the medical test agents."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Optional

import typer

from .config import PipelineConfig
from .pipeline import MedicalTestPipeline, PatientProfile

app = typer.Typer(help="Run the medical test agent pipeline")


@app.command()
def run(
    symptoms: str = typer.Option(..., help="Comma separated list of symptoms"),
    age: int = typer.Option(..., min=0, help="Patient age"),
    sex: str = typer.Option(..., help="Patient sex"),
    risk_factors: str = typer.Option("", help="Comma separated risk factors"),
    pregnant: bool = typer.Option(False, help="Whether the patient is currently pregnant"),
    renal_impairment: bool = typer.Option(False, help="Whether the patient has known renal impairment"),
    config_path: Optional[Path] = typer.Option(None, help="Optional path to a JSON configuration file"),
) -> None:
    """Run the medical test pipeline and print a textual report."""

    symptom_list = _split_csv(symptoms)
    risk_factor_list = _split_csv(risk_factors)
    flags = {
        "pregnant": str(pregnant).lower(),
        "renal_impairment": str(renal_impairment).lower(),
    }

    if config_path:
        data = json.loads(config_path.read_text())
        config = PipelineConfig.from_dict(data)
    else:
        config = PipelineConfig.load_default()

    pipeline = MedicalTestPipeline(config)
    report = pipeline.run(
        PatientProfile(
            age=age,
            sex=sex,
            symptoms=symptom_list,
            risk_factors=risk_factor_list,
            flags=flags,
        )
    )
    typer.echo(report)


def _split_csv(raw: str) -> list[str]:
    return [item.strip().lower() for item in raw.split(",") if item.strip()]


if __name__ == "__main__":
    app()
