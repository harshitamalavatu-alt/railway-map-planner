"""Command-line interface and route visualization for Railway Map Planner."""

import argparse
import sys
from typing import List
from ..algorithms.dijkstra import DijkstraRouter, RouteResult
from ..graph.network_loader import NetworkLoader
from ..graph.railway_graph import RailwayGraph


def format_table(headers: List[str], rows: List[List[str]]) -> str:
    """Formats ASCII table with column width padding."""
    col_widths = [len(h) for h in headers]
    for row in rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    sep = "+" + "+".join(["-" * (w + 2) for w in col_widths]) + "+"
    head_str = "| " + " | ".join([f"{h:<{col_widths[i]}}" for i, h in enumerate(headers)]) + " |"

    lines = [sep, head_str, sep]
    for row in rows:
        row_str = "| " + " | ".join([f"{str(cell):<{col_widths[i]}}" for i, cell in enumerate(row)]) + " |"
        lines.append(row_str)
    lines.append(sep)
    return "\n".join(lines)


def render_ascii_map(route: RouteResult) -> str:
    """Renders a schematic visual ASCII track diagram of the journey."""
    lines = ["\nRAILWAY SCHEMATIC ROUTE MAP:", "=" * 50]
    for i, st in enumerate(route.stations):
        if i == 0:
            lines.append(f"  [ORIGIN]      ● {st.name} ({st.code}) - {st.city}")
        elif i == len(route.stations) - 1:
            seg = route.segments[i - 1]
            lines.append(f"                │ [{seg.distance_km:.0f} km | {int(seg.duration_minutes)} min]")
            lines.append(f"  [DESTINATION] ◼ {st.name} ({st.code}) - {st.city}")
        else:
            seg = route.segments[i - 1]
            lines.append(f"                │ [{seg.distance_km:.0f} km | {int(seg.duration_minutes)} min]")
            lines.append(f"  [JUNCTION]    ○ {st.name} ({st.code}) - {st.city}")
    lines.append("=" * 50)
    return "\n".join(lines)


def display_route(route: RouteResult):
    """Prints complete route itinerary and summary."""
    print("\n" + "=" * 65)
    print(f" JOURNEY SUMMARY: {route.source_code} -> {route.destination_code}")
    print(f" Optimization Strategy: {route.weight_mode.upper()}")
    print(f" Total Track Distance: {route.total_distance_km:.1f} km")
    print(f" Estimated Travel Time: {route.total_hours_str} ({route.total_duration_minutes:.1f} mins)")
    print(f" Total Stops: {len(route.stations) - 1} hops across {len(route.stations)} stations")
    print("=" * 65)

    headers = ["Stop #", "Station Name", "Code", "Leg Dist (km)", "Cum Dist (km)", "Leg Time (min)", "Cum Time (min)"]
    rows = []

    # Origin row
    origin = route.stations[0]
    rows.append(["0", origin.name, origin.code, "0.0", "0.0", "0.0", "0.0"])

    for i, seg in enumerate(route.segments, start=1):
        rows.append([
            str(i),
            seg.destination.name,
            seg.destination.code,
            f"{seg.distance_km:.1f}",
            f"{seg.cumulative_distance_km:.1f}",
            f"{seg.duration_minutes:.1f}",
            f"{seg.cumulative_duration_minutes:.1f}",
        ])

    print("\nITINERARY BREAKDOWN:")
    print(format_table(headers, rows))
    print(render_ascii_map(route))


def run_cli():
    parser = argparse.ArgumentParser(description="Railway Map Planner - Shortest Route Finder")
    parser.add_argument("--from-station", "-f", help="Origin station code (e.g., NDLS)")
    parser.add_argument("--to-station", "-t", help="Destination station code (e.g., BCT)")
    parser.add_argument("--mode", "-m", choices=["distance", "duration"], default="distance", help="Optimization metric")
    parser.add_argument("--list-stations", action="store_true", help="List all indexed railway stations")
    parser.add_argument("--search", help="Search station by name or code")
    parser.add_argument("--data-file", default="data/railway_network.json", help="Path to network JSON")
    args = parser.parse_args()

    graph = NetworkLoader.load_from_json(args.data_file)

    if args.list_stations:
        stations = sorted(graph.get_all_stations(), key=lambda s: s.code)
        headers = ["Code", "Station Name", "City", "Zone", "Platforms", "Connections"]
        rows = [[s.code, s.name, s.city, s.zone, str(s.platforms), str(graph.degree(s.code))] for s in stations]
        print(f"\nINDEXED RAILWAY STATIONS ({len(stations)} total):")
        print(format_table(headers, rows))
        return

    if args.search:
        q = args.search.lower()
        matches = [s for s in graph.get_all_stations() if q in s.code.lower() or q in s.name.lower() or q in s.city.lower()]
        print(f"\nSearch results for '{args.search}':")
        for s in matches:
            print(f"  [{s.code}] {s.name} - {s.city} (Zone: {s.zone})")
        return

    if args.from_station and args.to_station:
        route = DijkstraRouter.find_shortest_path(
            graph,
            start_code=args.from_station,
            end_code=args.to_station,
            weight_mode=args.mode,
        )
        if route is None:
            print(f"\nError: No route exists between {args.from_station} and {args.to_station}.")
            sys.exit(1)
        display_route(route)
        return

    # Interactive mode default demo: NDLS to BCT
    print("\nRunning default route optimization: New Delhi (NDLS) -> Mumbai Central (BCT)")
    route = DijkstraRouter.find_shortest_path(graph, "NDLS", "BCT", weight_mode="distance")
    display_route(route)


if __name__ == "__main__":
    run_cli()
