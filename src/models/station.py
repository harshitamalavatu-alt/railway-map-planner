"""Railway Station node domain model."""

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Station:
    """Represents a station node in the railway transit network."""

    code: str
    name: str
    city: str
    zone: str
    platforms: int = 4

    def __post_init__(self):
        object.__setattr__(self, "code", self.code.strip().upper())

    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

    def __repr__(self) -> str:
        return f"Station(code='{self.code}', name='{self.name}', city='{self.city}')"
