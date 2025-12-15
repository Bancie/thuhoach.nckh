# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project overview

This repository contains research and experimentation around scheduling and location theory, with two main strands:
- Usage examples and supporting materials for the external `tilearn` Python library (installed from PyPI and documented at the links in `other/TiLearn_Folder/tilearn/Running Illustrative Data Using the TiLearn Library.md`).
- Standalone Python modules and notes for facility location and shortest-path experiments under `ipynb/location`, plus various research notes in Markdown under `RES/` and `notebook.md`.

Root-level `main.py` demonstrates running `tilearn.optimal_list` on a single CSV list of jobs and printing the resulting schedule. Most of the heavy lifting lives in the external `tilearn` package rather than this repo.

## Environment setup and common commands

### Python environment

From the repository root:

- (Optional but recommended) create a virtual environment:
  - `python -m venv .venv`
  - `source .venv/bin/activate` (macOS/Linux)
- Install dependencies:
  - `pip install -r requirements.txt`

The dependency list includes scientific/optimization libraries such as `ortools`, `numpy`, `scipy`, `networkx`, `geopandas`, and the external `tilearn` library.

### Running core scripts

All commands below assume you are in the repository root.

- Run the simple TiLearn example in `main.py`:
  - `python main.py`
  - Note: `main.py` currently uses hard-coded absolute file-system paths for `data`, `backup`, and `data1`. If you move the repository or want portability, adjust these paths to be relative to the project root before running.

- Run the location/optimization test script using OR-Tools:
  - `python ipynb/location/test/test.py`
  - This script currently generates a random transport cost matrix and (with some lines uncommented) can call `data_model.solver(...)` from `ipynb/location/packages/ortool.py` to solve a p-median-style model.

- Run the Tkinter GUI demo:
  - `python tkinter_test.py`
  - Opens a simple "Feet to Meters" converter window; this is self-contained and independent of the rest of the project.

### Tests and linting

There is no formal test framework or project-level linting configuration in this repository:
- "Tests" are ad-hoc scripts like `ipynb/location/test/test.py` that you run directly with `python`.
- No dedicated commands or configuration exist for tools like `pytest`, `unittest`, or linters/formatters. If you introduce such tooling, document the commands here.

## High-level architecture

### Root level

- `main.py` — Minimal driver script that:
  - Imports `tilearn as tl` and `from tilearn import _plat as pl`.
  - Defines absolute paths to a `data/` directory and a single CSV file (`data1.csv`).
  - Wraps that CSV in a `pl.List` instance and passes it to `tl.optimal_list` along with paths for an input and backup directory.
  - Iterates over and prints each row of the resulting schedule.

  This script is essentially a thin example client for the external `tilearn` package. Any nontrivial scheduling logic is in `tilearn` itself, not in this repo.

- `requirements.txt` — Pinned Python dependencies for running the experiments and demos. Notably includes:
  - Scientific stack: `numpy`, `scipy`, `pandas`, `matplotlib`, `networkx`, `sympy`.
  - Geospatial/graph stack: `osmnx`, `geopandas`, `rasterio`, `rtree`.
  - Optimization: `ortools`.
  - Domain library: `tilearn`.

- Documentation and notes:
  - `README.md` — Minimal, just names the repo (`thuhoach.nckh`).
  - `notebook.md` — Outline-style notes on the history of location theory and related optimization problems (p-median, p-center, covering problems, obnoxious facilities, etc.).
  - `RES/` — Miscellaneous mathematical notes and references (e.g., integer programming links, proofs, LaTeX snippets). These are background research materials and do not affect runtime behavior.

### `ipynb/location`: location theory and optimization code

This sub-tree contains the main in-repo Python logic for location and network experiments.

#### `ipynb/location/packages`

Core modules:

- `ShortestPath.py`
  - Defines a `Graph` class over an adjacency matrix (`self.graph`) with:
    - Dijkstra's algorithm (`dijkstra`) to compute shortest paths from a source node, maintaining distance and parent arrays.
    - `getShortestPath(src, dest)` to reconstruct and return the path (as a list of node indices) and its total distance.
  - This is used as the basic shortest-path engine in higher-level location algorithms.

- `GraphView.py`
  - Wraps an adjacency matrix in a `Graph` visualization helper built on `networkx` and `matplotlib`.
  - Key responsibilities:
    - `show()` constructs an undirected graph from the matrix, relabels nodes with letters (A, B, C, ...), and draws the graph with default layout and edge labels.
    - `show_node(show_marks=True)` relabels nodes as `v1`, `v2`, ..., stores the `networkx` graph and node positions, and can overlay "marked points" along edges.
    - `add_marked_point_on_edge(u, v, alpha, label, color)` records a point along edge `(u, v)` at a fractional position `alpha` between the endpoints for later display in `show_node`.
  - Use this when you need to visualize graphs and specific candidate facility locations or breakpoints on edges.

- `Point.py`
  - Houses several classes related to 1-median/center-type problems on graphs and to analyzing piecewise-linear functions built from distances:
    - `FunctionPlotter` — Manages a set of 1D functions, evaluates them on a common `x` grid, and:
      - Plots them together, optionally highlighting intersection points.
      - Uses `scipy.optimize.fsolve` to compute intersection points between two functions and records them for later plotting.
    - `GlobalCenter` — Given a `sourceGraph` (adjacency matrix) and number of vertices, performs a global search over all unordered vertex pairs `(i, j)`:
      - Constructs a local-minimum object for each pair and computes its local objective value.
      - Tracks and returns the best (minimum) value and the corresponding vertex pair.
    - `Local` — Extends `GlobalCenter` with:
      - Overloaded `distance` methods (via `multipledispatch`) that accept either vertex labels as characters (`'A'`, `'B'`, ...) or integer indices, internally delegating to `ShortestPath.Graph.getShortestPath`.
      - `abstractAlpha(A, B)`, `BottleNeck(A)`, and `EquiPoint(A, B)` to analyze positions along edge `(vertex_i, vertex_j)` where ordered distance relationships hold.
    - `BoLocalMin` — Adds bounding logic:
      - `upperlm(A)` and `lowerlm(A)` compute upper and lower bounding lines for a vertex `A` based on distances to the two edge endpoints.
      - `BoundedValue('upper'|'lower')` iterates over vertices to compute the maximum value over those bounds.
    - `InLocalMin` — Manages a collection of linear functions built from distances:
      - `add_line`, `show_lines`, and `upper_envelope` for building and evaluating a piecewise-linear upper envelope.
      - `intersect` and `BreakpointList` to find intersection abscissas between pairs of lines.
      - `lineList` builds the specific distance-based lines for all vertices except the two edge endpoints.
      - `IntervalValue` computes candidate breakpoints (including 0 and the endpoint distance) and returns the minimum value of the upper envelope across them.
    - `LocalMinima` — Multiple-inheritance class combining `BoLocalMin`, `InLocalMin`, and `GlobalCenter` to:
      - Compute an overall local minimum criterion by comparing upper/lower bounds and the interval minimum (`LocalMinVal`).
  - Together, these classes support detailed analysis of candidate facility locations along edges of a graph, using shortest-path distances and piecewise-linear envelopes.

- `ortool.py`
  - Defines a `data_model` class encapsulating a p-median-style integer programming model using OR-Tools:
    - Initialized with a `cost_matrix` and `p_facility` (number of facilities to open).
    - `create_data_model()` builds:
      - Equality constraints to ensure each demand node is assigned exactly once and exactly `p_facility` facilities are opened (diagonal assignment constraints).
      - Inequality constraints linking assignment decisions to facility-opening decisions ("you can only assign to an open facility").
      - A flattened objective coefficient vector from the cost matrix.
    - `solver(is_maximization=True, is_integer=False)` sets up a `pywraplp.Solver` instance, defines variables, adds constraints, and optimizes the objective:
      - Returns the number of variables, solver version, objective value, solution matrix (reshaped from flat variables), and basic performance statistics.
  - The design assumes a square cost matrix (same number of demand points and candidate facility locations).

#### `ipynb/location/test`

- `test.py` — Simple script that:
  - Extends `sys.path` so that `ipynb/location/packages` can be imported as `from packages.ortool import data_model` when run as a script.
  - Generates a random integer cost matrix with zero diagonals.
  - (Commented code) shows how to instantiate `data_model` with a chosen `p_facility` and call `.solver(is_maximization=False, is_integer=True)` to solve a p-median problem.

  This is best viewed as an executable example for the OR-Tools-based p-median model, not as part of a structured test suite.

### TiLearn usage materials (`other/TiLearn_Folder` and related)

The `other/TiLearn_Folder` directory contains narrative documentation and example code showing how to use the external `tilearn` library with CSV datasets:

- `tilearn/Running Illustrative Data Using the TiLearn Library.md` outlines:
  - Installation of `tilearn` via `%pip install tilearn` and supporting analysis libraries.
  - The expected folder structures for illustrative data (`tilearn/data/`, `tilearn/data_project/` with nested `backup/` directories).
  - How to construct lists of `pl.List` objects (with `prec` flags indicating whether precedence constraints are present) and call `tl.optimal_list(...)` to obtain optimized schedules for different job sets.
  - How to write the resulting schedule to CSV and visualize it using `pandas` and `matplotlib`.

These materials treat this repository as a working directory for TiLearn examples and demonstrations rather than as the implementation of TiLearn itself.

### Miscellaneous utilities and demos

- `tkinter_test.py` — Standalone Tkinter GUI example; safe to modify or remove without affecting the optimization/location code.
- `other/random_value/` and similar folders — Contain helper scripts (for example, generating random CSV job lists) that support experiments documented in the TiLearn markdown file.

## Guidance for future Warp agents

- When modifying or extending scheduling behavior driven by `tilearn`, prefer to:
  - Treat `tilearn` as an external dependency and write wrapper scripts, data preparation utilities, or analysis/visualization code in this repo.
  - Avoid re-implementing TiLearn internals here unless you are intentionally diverging from the upstream library.
- If you introduce new experiments in `ipynb/location`, keep the patterns consistent:
  - Put reusable algorithms in `ipynb/location/packages/`.
  - Add small, script-style drivers (like `test.py`) under `ipynb/location/test/` instead of embedding logic in notebooks only.
- Before adding any project-wide tooling (pytest, linters, type checkers), check this file and extend the "Environment setup and common commands" section with the exact commands you expect Warp to use.
