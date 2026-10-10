"""Dijkstra's shortest path algorithm implementation using priority queues."""

import heapq
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from ..graph.railway_graph import RailwayGraph
from ..models.station import Station
from ..models.track import Track


@dataclass
class RouteSegment:
    """Detailed hop-by-hop information along a path."""
    source: Station
    destination: Station
    distance_km: float
    duration_minutes: float
    cumulative_distance_km: float
    cumulative_duration_minutes: float


@dataclass
class RouteResult:
    """Encapsulates the complete optimized journey between two stations."""
    source_code: str
    destination_code: str
    weight_mode: str
    total_distance_km: float
    total_duration_minutes: float
    stations: List[Station]
    segments: List[RouteSegment]

    @property
    def total_hours_str(self) -> str:
        hours = int(self.total_duration_minutes // 60)
        mins = int(self.total_duration_minutes % 60)
        return f"{hours}h {mins}m"


class DijkstraRouter:
    """Executes Dijkstra's algorithm over RailwayGraph with Min-Heap Priority Queue.

    Time Complexity: O((V + E) log V)
    Space Complexity: O(V)
    """

    @staticmethod
    def find_shortest_path(
        graph: RailwayGraph,
        start_code: str,
        end_code: str,
        weight_mode: str = "distance",
    ) -> Optional[RouteResult]:
        """Finds the shortest path between start and end stations.

        Args:
            graph: The railway graph
            start_code: Origin station code
            end_code: Destination station code
            weight_mode: 'distance' (default, minimizing km) or 'duration' (minimizing travel time)

        Returns:
            RouteResult with complete path details or None if disconnected.
        """
        start = start_code.strip().upper()
        end = end_code.strip().upper()

        if not graph.get_station(start):
            raise KeyError(f"Origin station '{start}' not found in network.")
        if not graph.get_station(end):
            raise KeyError(f"Destination station '{end}' not found in network.")

        if start == end:
            st = graph.get_station(start)
            return RouteResult(
                source_code=start,
                destination_code=end,
                weight_mode=weight_mode,
                total_distance_km=0.0,
                total_duration_minutes=0.0,
                stations=[st],
                segments=[],
            )

        # Distances map: station_code -> best cost found
        distances: Dict[str, float] = {code: float("inf") for code in [s.code for s in graph.get_all_stations()]}
        distances[start] = 0.0

        # Predecessor mapping: station_code -> (prev_code, Track)
        previous: Dict[str, Tuple[Optional[str], Optional[Track]]] = {start: (None, None)}

        # Priority Queue: stores tuples of (current_cost, station_code)
        pq: List[Tuple[float, str]] = [(0.0, start)]

        visited = set()

        while pq:
            curr_cost, curr_node = heapq.heappop(pq)

            if curr_node in visited:
                continue
            visited.add(curr_node)

            if curr_node == end:
                break

            for track in graph.get_neighbors(curr_node):
                neighbor = track.destination
                if neighbor in visited:
                    continue

                edge_cost = track.distance_km if weight_mode == "distance" else track.duration_minutes
                new_cost = curr_cost + edge_cost

                if new_cost < distances.get(neighbor, float("inf")):
                    distances[neighbor] = new_cost
                    previous[neighbor] = (curr_node, track)
                    heapq.heappush(pq, (new_cost, neighbor))

        # Check if destination was reached
        if end not in previous:
            return None

        # Reconstruct path backwards
        station_codes: List[str] = []
        tracks_used: List[Track] = []
        curr = end

        while curr is not None:
            station_codes.append(curr)
            prev_node, edge = previous[curr]
            if edge is not None:
                tracks_used.append(edge)
            curr = prev_node

        station_codes.reverse()
        tracks_used.reverse()

        # Build detailed segments
        stations = [graph.get_station(code) for code in station_codes]
        segments: List[RouteSegment] = []
        cum_dist = 0.0
        cum_dur = 0.0

        for edge in tracks_used:
            cum_dist += edge.distance_km
            cum_dur += edge.duration_minutes
            segments.append(
                RouteSegment(
                    source=graph.get_station(edge.source),
                    destination=graph.get_station(edge.destination),
                    distance_km=edge.distance_km,
                    duration_minutes=edge.duration_minutes,
                    cumulative_distance_km=cum_dist,
                    cumulative_duration_minutes=cum_dur,
                )
            )

        total_dist = sum(t.distance_km for t in tracks_used)
        total_dur = sum(t.duration_minutes for t in tracks_used)

        return RouteResult(
            source_code=start,
            destination_code=end,
            weight_mode=weight_mode,
            total_distance_km=round(total_dist, 2),
            total_duration_minutes=round(total_dur, 2),
            stations=stations,
            segments=segments,
        )
