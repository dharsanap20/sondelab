# sondelab
An open-source platform for testing the reliability, consistency, accuracy, and robustness of large language models.

## Stage 1 — offline experiment prototype

The pilot asks one question using two wordings and two context conditions.
With two trials per combination, the engine sends eight requests to a local
mock connector. Its scripted reply is always `" PARIS "`. The pilot exercises
the evaluation software. Measuring real model behavior requires a live connector
and an independently validated dataset.

### Run the pilot

From the repository root, with Python 3.11 or later installed:

```sh
python -m examples.run_example
```

Open the JSON file printed by the command. Each run includes the exact prompt,
raw response, UTC timestamps, condition names, trial number and evaluation.
Connector failures have an error message and a null evaluation. The report
also includes the test case, provider, model ID and scheduling seed.

Edit `examples/pilot.json` to change the question, expected answer or conditions.
For five trials per combination in a repeatable shuffled order, run:

```sh
python -m examples.run_example --trials 5 --seed 7
```

The seed controls execution order. The evaluator ignores case and differences
in whitespace. It preserves punctuation and scores whole answers, so a correct
answer expressed as a longer sentence can fail this simple check.

### Run the tests

Create and activate a virtual environment, then install the test dependency.
In Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[test]"
.\.venv\Scripts\python -m pytest
```

On macOS or Linux, use `.venv/bin/python` for the last two commands.
