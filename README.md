# Railway Map Planner

![Python 3](https://img.shields.io/badge/Python-3.9%2B-blue.svg)
![Algorithms](https://img.shields.io/badge/Dijkstra-Min--Heap-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-brightgreen.svg)

A high-performance railway transit network router that models interconnected stations and rail lines as weighted directed/undirected graphs. Employs Dijkstra's Algorithm with binary min-heaps to solve shortest distance and minimum travel duration queries.

---

## Key Highlights

- **Weighted Graph Architecture**:
  - Vertex representation of railway stations with metadata (code, city, zone, platforms).
  - Edge representation of tracks with track distance (km), average speed (km/h), calculated travel time, and electrification.
  - Adjacency list storage ensuring optimal space efficiency: $O(V + E)$.
- **Dijkstra's Algorithm with Min-Heap**:
  - Implements priority-queue driven Dijkstra routing in $O((V + E) \log V)$ time complexity.
  - Dual optimization objective modes:
    - **Shortest Distance Mode**: Minimizes total kilometers traversed.
    - **Fastest Travel Time Mode**: Minimizes journey duration in minutes based on segment operating speeds.
- **Interactive Terminal Suite**:
  - Station code fuzzy search and station index catalog.
  - Hop-by-hop itinerary tables with per-leg and cumulative metrics.
  - ASCII terminal schematic journey visualization.
- **Comprehensive Network Dataset**:
  - Preloaded with major Indian Railways junction networks (New Delhi, Mumbai, Kolkata, Chennai, Bengaluru, Hyderabad, Ahmedabad, etc.).

---

## Algorithmic & Complexity Analysis

Let $G = (V, E)$ where $V$ represents station vertices and $E$ represents bidirectional railway tracks:

| Operation | Time Complexity | Space Complexity | Description |
|---|---|---|---|
| **Add Station** | $O(1)$ | $O(1)$ | Hash table insertion |
| **Add Track** | $O(1)$ | $O(1)$ | Adjacency list edge append |
| **Neighbor Query** | $O(1)$ | $O(1)$ | Direct adjacency lookup |
| **Dijkstra Shortest Path** | $O((V + E) \log V)$ | $O(V)$ | Priority Queue Min-Heap traversal |
| **Path Reconstruction** | $O(V)$ | $O(V)$ | Predecessor back-tracking |

---

## Directory Structure

```
railway-map-planner/
├── data/
│   └── railway_network.json   # 31+ stations and inter-city rail tracks
├── src/
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── dijkstra.py        # Min-heap Dijkstra shortest-path engine
│   │   └── k_shortest_paths.py# Alternative route suggestions
│   ├── cli/
│   │   ├── __init__.py
│   │   └── route_finder_cli.py# Terminal query interface & ASCII map
│   ├── graph/
│   │   ├── __init__.py
│   │   ├── network_loader.py  # JSON graph parser
│   │   └── railway_graph.py   # Adjacency list graph model
│   └── models/
│       ├── __init__.py
│       ├── station.py         # Station node entity
│       └── track.py           # Track edge entity
├── tests/
│   ├── __init__.py
│   └── test_dijkstra.py       # Unit test suite
├── main.py                    # CLI entrypoint
├── requirements.txt
└── README.md
```

---

## Usage Guide

### 1. Find Route Between Stations
Find the shortest route between New Delhi (`NDLS`) and Mumbai Central (`BCT`):
```bash
python3 main.py --from-station NDLS --to-station BCT --mode distance
```

Sample output:
```text
=================================================================
 JOURNEY SUMMARY: NDLS -> BCT
 Optimization Strategy: DISTANCE
 Total Track Distance: 1384.0 km
 Estimated Travel Time: 13h 58m (838.6 mins)
 Total Stops: 4 hops across 5 stations
=================================================================

ITINERARY BREAKDOWN:
+--------+----------------+------+---------------+---------------+----------------+----------------+
| Stop # | Station Name   | Code | Leg Dist (km) | Cum Dist (km) | Leg Time (min) | Cum Time (min) |
+--------+----------------+------+---------------+---------------+----------------+----------------+
| 0      | New Delhi      | NDLS | 0.0           | 0.0           | 0.0            | 0.0            |
| 1      | Kota Jn        | KOTA | 465.0         | 465.0         | 253.6          | 253.6          |
| 2      | Vadodara Jn    | BRC  | 526.0         | 991.0         | 332.2          | 585.8          |
| 3      | Surat          | ST   | 130.0         | 1121.0        | 86.7           | 672.5          |
| 4      | Mumbai Central | BCT  | 263.0         | 1384.0        | 166.1          | 838.6          |
+--------+----------------+------+---------------+---------------+----------------+----------------+

RAILWAY SCHEMATIC ROUTE MAP:
==================================================
  [ORIGIN]      ● New Delhi (NDLS) - Delhi
                │ [465 km | 253 min]
  [JUNCTION]    ○ Kota Jn (KOTA) - Kota
                │ [526 km | 332 min]
  [JUNCTION]    ○ Vadodara Jn (BRC) - Vadodara
                │ [130 km | 86 min]
  [JUNCTION]    ○ Surat (ST) - Surat
                │ [263 km | 166 min]
  [DESTINATION] ◼ Mumbai Central (BCT) - Mumbai
==================================================
```

### 2. Search Stations & List Network Catalog
```bash
# Search for a station
python3 main.py --search "Hyderabad"

# List all 31 indexed stations
python3 main.py --list-stations
```

### 3. Run Test Suite
```bash
python3 -m unittest discover tests
```

---

## License
MIT License.
