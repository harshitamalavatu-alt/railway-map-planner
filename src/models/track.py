"""Railway Track edge domain model."""

from dataclasses import dataclass


@dataclass
class Track:
    """Represents a directional weighted railway track connection between two stations."""

    source: str
    destination: str
    distance_km: float
    avg_speed_kmh: float = 80.0
    electrified: bool = True

    def __post_init__(self):
        self.source = self.source.strip().upper()
        self.destination = self.destination.strip().upper()

    @property
    def duration_minutes(self) -> float:
        """Calculates transit time in minutes."""
        if self.avg_speed_kmh <= 0:
            return 0.0
        return (self.distance_km / self.avg_speed_kmh) * 60.0

    def __repr__(self) -> str:
        return (
            f"Track({self.source} -> {self.destination}, {self.distance_km:.1f} km, "
            f"{self.duration_minutes:.1f} min)"
        )
