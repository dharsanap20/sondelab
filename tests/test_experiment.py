import json
from itertools import product

import pytest

from sondelab.connectors.base import ConnectorError
from sondelab.connectors.mock import MockConnector
from sondelab.engine import run_experiment
from sondelab.evaluators.text_match import evaluate
from sondelab.models import Case, Condition
from sondelab.reports.json_report import save_report


@pytest.fixture
def case():
    return Case("pilot", "Paris", (Condition("a", "Capital?"), Condition("b", "Which city?")),
                (Condition("none", ""), Condition("hint", "In France.")))


def test_schedule_and_report(case, tmp_path):
    experiment = run_experiment(case, MockConnector(" PARIS "), trials=3, seed=5)
    path = tmp_path / "results" / "pilot.json"
    save_report(experiment, path)
    report = json.loads(path.read_text(encoding="utf-8"))
    runs = report["runs"]
    keys = [(r["wording"], r["context"], r["trial"]) for r in runs]
    assert sorted(keys) == sorted(product(["a", "b"], ["none", "hint"], range(1, 4)))
    repeat = run_experiment(case, MockConnector(" PARIS "), trials=3, seed=5)
    assert keys == [(r.wording, r.context, r.trial) for r in repeat.runs]
    assert report["provider"] == "local-mock"
    for run in runs:
        question = "Capital?" if run["wording"] == "a" else "Which city?"
        expected = question if run["context"] == "none" else f"Context:\nIn France.\n\nQuestion:\n{question}"
        assert run["prompt_sent"] == expected
        assert run["response"] == " PARIS "
        assert run["evaluation"] == {"passed": True, "version": "normalized-text-v1"}
    with pytest.raises(FileExistsError):
        save_report(experiment, path)


def test_error_preserved_and_remaining_calls_scored(case):
    class Intermittent:
        provider = "test"
        model_id = "test"
        calls = 0

        def generate(self, prompt):
            self.calls += 1
            if self.calls == 1:
                raise ConnectorError("Timeout")
            return "London"

    first, *rest = run_experiment(case, Intermittent(), 1).runs
    assert first.error == "Timeout"
    assert first.evaluation is None and first.response is None
    assert len(rest) == 3
    assert all(r.error is None and r.evaluation.passed is False for r in rest)


@pytest.mark.parametrize("trials", [0, -1, True, 1.5])
def test_invalid_trials(case, trials):
    with pytest.raises(ValueError):
        run_experiment(case, MockConnector("Paris"), trials)


def test_normalization_preserves_meaningful_symbols():
    assert evaluate(" New\n  York ", "new york").passed
    assert not evaluate("-1", "1").passed
