import argparse
import json
from pathlib import Path
from uuid import uuid4

from sondelab.connectors.mock import MockConnector
from sondelab.engine import run_experiment
from sondelab.models import Case, Condition
from sondelab.reports.json_report import save_report


def main():
    parser = argparse.ArgumentParser(description="Run SondeLab's offline mock experiment.")
    parser.add_argument("--trials", type=int, default=2)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    data = json.loads(Path(__file__).with_name("pilot.json").read_text(encoding="utf-8"))
    case = Case(data["name"], data["expected"],
                tuple(Condition(**item) for item in data["prompts"]),
                tuple(Condition(**item) for item in data["contexts"]))
    experiment = run_experiment(case, MockConnector(" PARIS "), args.trials, args.seed)
    path = args.output or Path("outputs") / f"pilot-{uuid4().hex}.json"
    save_report(experiment, path)
    print(f"Saved {len(experiment.runs)} mock trials to {path}")


if __name__ == "__main__":
    main()
