from sondelab.models import Evaluation


def normalize(text: str) -> str:
    return " ".join(text.casefold().split())


def evaluate(response: str, expected: str) -> Evaluation:
    return Evaluation("normalized-text-v1", normalize(response) == normalize(expected))
