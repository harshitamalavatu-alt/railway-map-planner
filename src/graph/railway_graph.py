"""Adjacency list weighted graph representation of the railway network."""

from typing import Dict, List, Optional, Set
from ..models.station import Station
from ..models.track import Track


class RailwayGraph:
    """Represents the railway network as a directed/undirected weighted graph.

    Maintains stations as vertices and tracks as weighted edges stored in an
    adjacency list structure for optimal graph search and shortest path calculation.
    """

    def __init__(self):
        self._stations: Dict[str, Station] = {}
        self._adj: Dict[str, List[Track]] = {}

    def add_station(self, station: Station):
        """Adds a station vertex to the network."""
        code = station.code.upper()
        self._stations[code] = station
        if code not in self._adj:
            self._adj[code] = []

    def add_track(
        self,
        source: str,
        destination: str,
        distance_km: float,
        avg_speed_kmh: float = 80.0,
        electrified: bool = True,
        bidirectional: bool = True,
    ):
        """Adds a track connection between two stations."""
        src = source.strip().upper()
        dst = destination.strip().upper()

        if src not in self._stations:
            raise KeyError(f"Source station '{src}' does not exist in graph.")
        if dst not in self._stations:
            raise KeyError(f"Destination station '{dst}' does not exist in graph.")

        forward_track = Track(src, dst, distance_km, avg_speed_kmh, electrified)
        self._adj[src].append(forward_track)

        if bidirectional:
            reverse_track = Track(dst, src, distance_km, avg_speed_kmh, electrified)
            self._adj[dst].append(reverse_track)

    def get_station(self, code: str) -> Optional[Station]:
        """Retrieves station metadata by station code."""
        return self._stations.get(code.strip().upper())

    def get_neighbors(self, code: str) -> List[Track]:
        """Returns outgoing tracks from a station."""
        return self._adj.get(code.strip().upper(), [])

    def get_all_stations(self) -> List[Station]:
        """Returns list of all stations in the network."""
        return list(self._stations.values())

    def station_count(self) -> int:
        return len(self._stations)

    def track_count(self) -> int:
        """Returns total directional track segments."""
        return sum(len(edges) for edges in self._adj.values())

    def degree(self, code: str) -> int:
        """Returns station degree (number of connected lines)."""
        return len(self.get_neighbors(code))
