from datetime import datetime, timezone
from itertools import product
from random import Random

from sondelab.connectors.base import Connector, ConnectorError
from sondelab.evaluators.text_match import evaluate
from sondelab.models import Case, Experiment, Run
from sondelab.prompt_builder import build_prompt


def run_experiment(case: Case, connector: Connector, trials: int, seed: int = 0) -> Experiment:
    if type(trials) is not int or trials < 1:
        raise ValueError("trials must be a positive integer")
    schedule = list(product(case.prompts, case.contexts, range(1, trials + 1)))
    Random(seed).shuffle(schedule)
    runs = []
    for wording, context, trial in schedule:
        prompt = build_prompt(wording.text, context.text)
        started = datetime.now(timezone.utc).isoformat()
        response = error = evaluation = None
        try:
            response = connector.generate(prompt)
        except ConnectorError as exc:
            error = str(exc)
        else:
            evaluation = evaluate(response, case.expected)
        runs.append(Run(
            wording=wording.name, context=context.name, trial=trial,
            prompt_sent=prompt, started_at=started,
            completed_at=datetime.now(timezone.utc).isoformat(),
            response=response, error=error, evaluation=evaluation,
        ))
    return Experiment(case, connector.provider, connector.model_id, trials, seed, runs)
