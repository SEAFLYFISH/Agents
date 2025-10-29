from pathlib import Path

from medical_test_agents.agents.diagnostic_recommender import DiagnosticTestRecommenderAgent
from medical_test_agents.agents.symptom_checker import ConditionScore, SymptomCheckerAgent, SymptomCheckerInput
from medical_test_agents.config import PipelineConfig
from medical_test_agents.knowledge_base import MedicalKnowledgeBase
from medical_test_agents.pipeline import MedicalTestPipeline, PatientProfile


def load_config() -> PipelineConfig:
    return PipelineConfig(knowledge_base_path=Path(__file__).resolve().parent.parent / "data" / "medical_knowledge.json")


def test_symptom_checker_scores_conditions():
    config = load_config()
    kb = MedicalKnowledgeBase.load(config.knowledge_base_path)
    agent = SymptomCheckerAgent(config.agent)

    result = agent.run(
        kb.iter_conditions(),
        SymptomCheckerInput(symptoms=["fever", "cough"], risk_factors=["smoker"]),
    )

    scores = result.details["scores"]
    influenza = next(item for item in scores if item["condition"] == "Influenza")
    pneumonia = next(item for item in scores if item["condition"] == "Pneumonia")

    assert influenza["score"] > 0
    assert pneumonia["score"] >= influenza["score"]


def test_test_recommender_applies_threshold_and_contraindications():
    config = load_config()
    kb = MedicalKnowledgeBase.load(config.knowledge_base_path)
    symptom_agent = SymptomCheckerAgent(config.agent)
    test_agent = DiagnosticTestRecommenderAgent(config.agent)

    symptom_result = symptom_agent.run(
        kb.iter_conditions(),
        SymptomCheckerInput(symptoms=["dysuria", "frequency"], risk_factors=["pregnant"]),
    )
    scores = symptom_result.details["scores"]

    recommendations = test_agent.run(
        kb.iter_conditions(),
        [ConditionScore(**score) if isinstance(score, dict) else score for score in scores],
        {"renal_impairment": "true"},
    )

    recs = recommendations.details["recommendations"]
    uti_recs = [rec for rec in recs if rec["condition"] == "Urinary Tract Infection"]
    assert any(rec["contraindicated"] for rec in uti_recs)


def test_pipeline_returns_report_string():
    config = load_config()
    pipeline = MedicalTestPipeline(config)

    report = pipeline.run(
        PatientProfile(
            age=65,
            sex="female",
            symptoms=["fever", "cough"],
            risk_factors=["elderly"],
            flags={"pregnant": "false", "renal_impairment": "false"},
        )
    )

    assert "Medical Test Recommendation Report" in report
    assert "Test recommendations:" in report
