# Medical Test Agents

Medical Test Agents is a modular agent-based system that helps triage patient-reported symptoms,
estimate likely conditions, and recommend diagnostic medical tests. The project is designed as an
example of an interpretable and auditable orchestration pipeline built in pure Python.

## Features

- ✅ **Symptom normalization** using curated vocabularies.
- 🧠 **Probabilistic condition scoring** based on symptom weights and patient risk factors.
- 🧾 **Test recommendation** with structured rationales and contraindication checks.
- 🪄 **Report generation** that summarizes the reasoning steps for clinical review.
- 🛠️ **Composable agents** that can be reused and extended for custom workflows.

## Installation

```bash
pip install -e .
```

## Usage

```bash
medical-test-agents run --symptoms "fever,cough" --age 45 --sex female
```

This command will print a textual report describing the triage reasoning and the recommended
laboratory or imaging tests.

## Development

Run the unit test suite with:

```bash
pytest
```

## Project Layout

```
medical_test_agents/
├── agents/
│   ├── base.py                  # Common abstractions
│   ├── diagnostic_recommender.py
│   └── symptom_checker.py
├── cli.py                       # Command line entrypoints
├── config.py                    # Settings and constants
├── knowledge_base.py            # Utilities for loading medical knowledge data
└── pipeline.py                  # Orchestration for the end-to-end flow
```

Supporting files such as `data/medical_knowledge.json` contain the curated medical knowledge used by
the agents. Tests live in the `tests/` folder.

## License

MIT
