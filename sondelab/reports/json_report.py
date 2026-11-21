import json
from dataclasses import asdict
from pathlib import Path

from sondelab.models import Experiment


def save_report(experiment: Experiment, path: Path) -> None:
    data = {"schema_version": 1, **asdict(experiment)}
    payload = json.dumps(data, indent=2, ensure_ascii=False)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8") as stream:
        stream.write(payload + "\n")
