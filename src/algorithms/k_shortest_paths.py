"""Alternative route finding using edge penalty heuristic."""

from typing import List, Optional
from ..graph.railway_graph import RailwayGraph
from .dijkstra import DijkstraRouter, RouteResult


class RouteAlternativesFinder:
    """Finds alternative distinct routes between railway stations."""

    @staticmethod
    def find_alternatives(
        graph: RailwayGraph,
        start_code: str,
        end_code: str,
        max_routes: int = 2,
    ) -> List[RouteResult]:
        """Finds primary and secondary distinct routing paths."""
        results: List[RouteResult] = []

        # 1. Best path by distance
        dist_route = DijkstraRouter.find_shortest_path(graph, start_code, end_code, weight_mode="distance")
        if dist_route:
            results.append(dist_route)

        # 2. Best path by travel time (duration)
        time_route = DijkstraRouter.find_shortest_path(graph, start_code, end_code, weight_mode="duration")
        if time_route:
            # Check if route is distinct
            if not results or [s.code for s in time_route.stations] != [s.code for s in results[0].stations]:
                results.append(time_route)

        return results[:max_routes]
