from dataclasses import dataclass


@dataclass(frozen=True)
class MockConnector:
    """Return the same scripted text for every input without using a network."""

    reply: str
    provider = "local-mock"
    model_id = "fixed-reply-v1"

    def generate(self, prompt: str) -> str:
        return self.reply
