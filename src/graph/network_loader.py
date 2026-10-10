"""Loader and validator for railway graph network datasets."""

import json
import os
from typing import Optional
from ..models.station import Station
from .railway_graph import RailwayGraph


class NetworkLoader:
    """Loads railway network definitions from JSON files into graph instances."""

    @staticmethod
    def load_from_json(json_path: str = "data/railway_network.json") -> RailwayGraph:
        """Parses station nodes and track edges from JSON into RailwayGraph."""
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Network file not found at: {json_path}")

        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        graph = RailwayGraph()

        for s_data in data.get("stations", []):
            station = Station(
                code=s_data["code"],
                name=s_data["name"],
                city=s_data["city"],
                zone=s_data.get("zone", "IR"),
                platforms=s_data.get("platforms", 4),
            )
            graph.add_station(station)

        for t_data in data.get("tracks", []):
            graph.add_track(
                source=t_data["source"],
                destination=t_data["destination"],
                distance_km=float(t_data["distance_km"]),
                avg_speed_kmh=float(t_data.get("avg_speed_kmh", 80.0)),
                electrified=bool(t_data.get("electrified", True)),
                bidirectional=True,
            )

        return graph
