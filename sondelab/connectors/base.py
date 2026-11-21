from typing import Protocol


class ConnectorError(Exception):
    """A model call failed. The message must be safe to include in a report."""


class Connector(Protocol):
    provider: str
    model_id: str

    def generate(self, prompt: str) -> str:
        """Return unedited response text or raise ConnectorError."""
        ...
