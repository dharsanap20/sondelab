from dataclasses import dataclass


@dataclass(frozen=True)
class Condition:
    name: str
    text: str


@dataclass(frozen=True)
class Case:
    name: str
    expected: str
    prompts: tuple[Condition, ...]
    contexts: tuple[Condition, ...]

    def __post_init__(self):
        if not self.name.strip() or not self.expected.strip():
            raise ValueError("A case needs a name and an expected answer.")
        for conditions in (self.prompts, self.contexts):
            names = [condition.name for condition in conditions]
            if not names or any(not name.strip() for name in names) or len(set(names)) != len(names):
                raise ValueError("Each condition group needs unique, nonempty names.")
        if any(not prompt.text.strip() for prompt in self.prompts):
            raise ValueError("Prompt text must contain a question.")


@dataclass(frozen=True)
class Evaluation:
    version: str
    passed: bool


@dataclass(frozen=True)
class Run:
    wording: str
    context: str
    trial: int
    prompt_sent: str
    started_at: str
    completed_at: str
    response: str | None
    error: str | None
    evaluation: Evaluation | None


@dataclass(frozen=True)
class Experiment:
    case: Case
    provider: str
    model_id: str
    trials: int
    seed: int
    runs: list[Run]
