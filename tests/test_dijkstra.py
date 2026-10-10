"""Unit tests for Dijkstra shortest path algorithm and Railway Graph."""

import unittest

from src.algorithms.dijkstra import DijkstraRouter
from src.algorithms.k_shortest_paths import RouteAlternativesFinder
from src.graph.network_loader import NetworkLoader
from src.graph.railway_graph import RailwayGraph
from src.models.station import Station


class TestRailwayPlanner(unittest.TestCase):

    def setUp(self):
        # Create a controlled synthetic test graph
        self.g = RailwayGraph()
        self.sA = Station("A", "Station A", "City A", "Z1")
        self.sB = Station("B", "Station B", "City B", "Z1")
        self.sC = Station("C", "Station C", "City C", "Z1")
        self.sD = Station("D", "Station D", "City D", "Z1")
        self.sE = Station("E", "Isolated E", "City E", "Z1")

        for s in [self.sA, self.sB, self.sC, self.sD, self.sE]:
            self.g.add_station(s)

        # A -> B: 100 km at 100 km/h (60 min)
        # B -> D: 100 km at 100 km/h (60 min)
        # Total A -> B -> D: 200 km, 120 min
        self.g.add_track("A", "B", distance_km=100.0, avg_speed_kmh=100.0)
        self.g.add_track("B", "D", distance_km=100.0, avg_speed_kmh=100.0)

        # A -> C: 120 km at 150 km/h (48 min)
        # C -> D: 120 km at 150 km/h (48 min)
        # Total A -> C -> D: 240 km, 96 min
        self.g.add_track("A", "C", distance_km=120.0, avg_speed_kmh=150.0)
        self.g.add_track("C", "D", distance_km=120.0, avg_speed_kmh=150.0)

    def test_dijkstra_shortest_distance(self):
        # By distance: A -> B -> D is 200 km (vs 240 km for C)
        route = DijkstraRouter.find_shortest_path(self.g, "A", "D", weight_mode="distance")
        self.assertIsNotNone(route)
        self.assertEqual(route.total_distance_km, 200.0)
        codes = [s.code for s in route.stations]
        self.assertEqual(codes, ["A", "B", "D"])

    def test_dijkstra_fastest_duration(self):
        # By duration: A -> C -> D is 96 mins (vs 120 mins for B)
        route = DijkstraRouter.find_shortest_path(self.g, "A", "D", weight_mode="duration")
        self.assertIsNotNone(route)
        self.assertEqual(route.total_duration_minutes, 96.0)
        codes = [s.code for s in route.stations]
        self.assertEqual(codes, ["A", "C", "D"])

    def test_same_origin_destination(self):
        route = DijkstraRouter.find_shortest_path(self.g, "A", "A")
        self.assertIsNotNone(route)
        self.assertEqual(route.total_distance_km, 0.0)
        self.assertEqual(len(route.stations), 1)

    def test_disconnected_station(self):
        # E has no incoming or outgoing tracks
        route = DijkstraRouter.find_shortest_path(self.g, "A", "E")
        self.assertIsNone(route)

    def test_invalid_station_code(self):
        with self.assertRaises(KeyError):
            DijkstraRouter.find_shortest_path(self.g, "A", "XYZ")

    def test_alternative_paths(self):
        alts = RouteAlternativesFinder.find_alternatives(self.g, "A", "D", max_routes=2)
        self.assertEqual(len(alts), 2)
        # One should route via B and one via C
        p1 = [s.code for s in alts[0].stations]
        p2 = [s.code for s in alts[1].stations]
        self.assertNotEqual(p1, p2)

    def test_real_dataset_ndls_to_hwh(self):
        real_graph = NetworkLoader.load_from_json("data/railway_network.json")
        route = DijkstraRouter.find_shortest_path(real_graph, "NDLS", "HWH", weight_mode="distance")
        self.assertIsNotNone(route)
        self.assertEqual(route.source_code, "NDLS")
        self.assertEqual(route.destination_code, "HWH")
        self.assertGreater(route.total_distance_km, 1400.0)


if __name__ == "__main__":
    unittest.main()
