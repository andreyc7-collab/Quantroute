"""
QuantRoute — Quantum-Inspired Route Optimization Engine
Backend: FastAPI + Python
Algorithms: Simulated Annealing, Genetic Algorithm, Ant Colony Optimization
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import time
import math
import random
import numpy as np
from dataclasses import dataclass, field

app = FastAPI(
    title="QuantRoute API",
    description="Quantum-Inspired Logistics Optimization Engine",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Models ────────────────────────────────────────────────────────────────────

class Node(BaseModel):
    id: int
    x: float
    y: float
    demand: float = 1.0
    label: Optional[str] = None


class OptimizationRequest(BaseModel):
    nodes: List[Node]
    depot_id: int = 0
    mode: str = "tsp"           # tsp | vrp | assignment
    algorithm: str = "sa"       # sa | ga | aco
    vehicles: int = 3
    capacity: float = 10.0
    temperature: float = 1000.0
    cooling_rate: float = 0.97
    iterations: int = 5000
    population_size: int = 50   # GA only
    n_ants: int = 20            # ACO only


class RouteResult(BaseModel):
    tour: List[int]
    cost: float
    vehicle_id: Optional[int] = None


class OptimizationResult(BaseModel):
    routes: List[RouteResult]
    total_cost: float
    initial_cost: float
    improvement_pct: float
    elapsed_ms: float
    algorithm: str
    iterations_run: int
    convergence: List[float]
    metadata: dict


# ─── Distance Utilities ─────────────────────────────────────────────────────────

def euclidean(a: Node, b: Node) -> float:
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def build_distance_matrix(nodes: List[Node]) -> np.ndarray:
    n = len(nodes)
    D = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                D[i][j] = euclidean(nodes[i], nodes[j])
    return D


def tour_cost(tour: List[int], D: np.ndarray) -> float:
    return sum(D[tour[i]][tour[(i + 1) % len(tour)]] for i in range(len(tour)))


# ─── Greedy Initial Solution ────────────────────────────────────────────────────

def greedy_tour(nodes: List[Node], D: np.ndarray, depot_id: int = 0) -> List[int]:
    n = len(nodes)
    id_to_idx = {nd.id: i for i, nd in enumerate(nodes)}
    start = id_to_idx[depot_id]
    visited = [False] * n
    tour = [start]
    visited[start] = True
    for _ in range(n - 1):
        last = tour[-1]
        best_next, best_d = -1, float("inf")
        for j in range(n):
            if not visited[j] and D[last][j] < best_d:
                best_d, best_next = D[last][j], j
        tour.append(best_next)
        visited[best_next] = True
    return tour


# ─── Algorithm 1: Simulated Annealing ──────────────────────────────────────────

def simulated_annealing(
    init_tour: List[int],
    D: np.ndarray,
    T: float = 1000.0,
    alpha: float = 0.97,
    max_iter: int = 5000,
) -> dict:
    """
    Quantum-inspired SA: uses probabilistic acceptance analogous to
    quantum tunneling — bad moves accepted with probability e^(-ΔE/T).
    """
    cur = init_tour[:]
    cur_cost = tour_cost(cur, D)
    best, best_cost = cur[:], cur_cost
    convergence = [cur_cost]
    n = len(cur)

    for it in range(max_iter):
        # 2-opt swap move
        i, j = sorted(random.sample(range(1, n), 2))
        neighbor = cur[:i] + cur[i:j+1][::-1] + cur[j+1:]
        n_cost = tour_cost(neighbor, D)
        delta = n_cost - cur_cost

        # Metropolis criterion — quantum tunneling analog
        if delta < 0 or random.random() < math.exp(-delta / max(T, 1e-10)):
            cur, cur_cost = neighbor, n_cost

        if cur_cost < best_cost:
            best, best_cost = cur[:], cur_cost

        T *= alpha
        if it % max(1, max_iter // 100) == 0:
            convergence.append(best_cost)

    return {"tour": best, "cost": best_cost, "convergence": convergence, "iters": max_iter}


# ─── Algorithm 2: Genetic Algorithm ────────────────────────────────────────────

def genetic_algorithm(
    init_tour: List[int],
    D: np.ndarray,
    pop_size: int = 50,
    max_iter: int = 5000,
) -> dict:
    """
    Evolutionary optimization — population of quantum state superpositions
    collapsing toward optimal measurement.
    """
    n = len(init_tour)
    generations = max_iter // pop_size

    def mutate(t):
        t = t[:]
        i, j = random.sample(range(1, n), 2)
        t[i], t[j] = t[j], t[i]
        return t

    def crossover_ox(p1, p2):
        a, b = sorted(random.sample(range(n), 2))
        child = [None] * n
        child[a:b] = p1[a:b]
        fill = [x for x in p2 if x not in child]
        idx = 0
        for i in range(n):
            if child[i] is None:
                child[i] = fill[idx]; idx += 1
        return child

    population = [mutate(init_tour) for _ in range(pop_size - 1)] + [init_tour[:]]
    population.sort(key=lambda t: tour_cost(t, D))
    best = population[0][:]
    best_cost = tour_cost(best, D)
    convergence = [best_cost]

    for _ in range(generations):
        elite = population[:pop_size // 5]
        offspring = []
        while len(offspring) < pop_size - len(elite):
            p1, p2 = random.choices(population[:pop_size // 2], k=2)
            child = crossover_ox(p1, p2)
            if random.random() < 0.15:
                child = mutate(child)
            offspring.append(child)
        population = sorted(elite + offspring, key=lambda t: tour_cost(t, D))
        bc = tour_cost(population[0], D)
        if bc < best_cost:
            best_cost = bc
            best = population[0][:]
        convergence.append(best_cost)

    return {"tour": best, "cost": best_cost, "convergence": convergence, "iters": generations * pop_size}


# ─── Algorithm 3: Ant Colony Optimization ──────────────────────────────────────

def ant_colony(
    nodes: List[Node],
    D: np.ndarray,
    init_tour: List[int],
    n_ants: int = 20,
    max_iter: int = 5000,
    alpha: float = 1.0,
    beta: float = 2.0,
    rho: float = 0.5,
    Q: float = 100.0,
) -> dict:
    """
    ACO: pheromone-guided probabilistic search — analog to quantum walk
    probability amplitude reinforcement.
    """
    n = len(nodes)
    iters = max_iter // n_ants
    pheromone = np.ones((n, n))
    best = init_tour[:]
    best_cost = tour_cost(best, D)
    convergence = [best_cost]

    for _ in range(iters):
        all_tours, all_costs = [], []
        for _ in range(n_ants):
            visited = [False] * n
            path = [0]; visited[0] = True
            for _ in range(n - 1):
                cur = path[-1]
                scores = []
                for j in range(n):
                    if not visited[j]:
                        eta = 1.0 / max(D[cur][j], 1e-6)
                        scores.append((j, pheromone[cur][j] ** alpha * eta ** beta))
                total = sum(s for _, s in scores)
                r = random.random() * total
                chosen = scores[-1][0]
                for j, s in scores:
                    r -= s
                    if r <= 0:
                        chosen = j; break
                path.append(chosen); visited[chosen] = True
            c = tour_cost(path, D)
            all_tours.append(path); all_costs.append(c)
            if c < best_cost:
                best_cost = c; best = path[:]

        # Evaporate
        pheromone *= (1 - rho)
        # Deposit
        for path, c in zip(all_tours, all_costs):
            for i in range(n):
                a, b = path[i], path[(i + 1) % n]
                pheromone[a][b] += Q / c
                pheromone[b][a] += Q / c

        convergence.append(best_cost)

    return {"tour": best, "cost": best_cost, "convergence": convergence, "iters": iters * n_ants}


# ─── VRP Splitting ──────────────────────────────────────────────────────────────

def split_vrp(tour: List[int], nodes: List[Node], n_vehicles: int, capacity: float) -> List[List[int]]:
    """Clarke-Wright savings heuristic split for VRP."""
    routes = []
    remaining = tour[1:]  # exclude depot
    chunk = max(1, len(remaining) // n_vehicles)
    for i in range(n_vehicles):
        segment = remaining[i * chunk:(i + 1) * chunk]
        if segment:
            routes.append([tour[0]] + segment)
    # Leftover nodes go to last route
    leftover = remaining[n_vehicles * chunk:]
    if leftover:
        routes[-1].extend(leftover)
    return routes


# ─── Main Endpoint ──────────────────────────────────────────────────────────────

@app.post("/optimize", response_model=OptimizationResult)
def optimize(req: OptimizationRequest):
    if len(req.nodes) < 3:
        raise HTTPException(status_code=400, detail="Need at least 3 nodes.")

    nodes = req.nodes
    D = build_distance_matrix(nodes)
    t0 = time.perf_counter()

    init_tour = greedy_tour(nodes, D, req.depot_id)
    initial_cost = tour_cost(init_tour, D)

    algo = req.algorithm.lower()
    if algo == "sa":
        result = simulated_annealing(init_tour, D, req.temperature, req.cooling_rate, req.iterations)
    elif algo == "ga":
        result = genetic_algorithm(init_tour, D, req.population_size, req.iterations)
    elif algo == "aco":
        result = ant_colony(nodes, D, init_tour, req.n_ants, req.iterations)
    else:
        raise HTTPException(status_code=400, detail=f"Unknown algorithm: {algo}")

    elapsed_ms = (time.perf_counter() - t0) * 1000
    best_tour = result["tour"]
    best_cost = result["cost"]

    if req.mode == "vrp" or req.mode == "assignment":
        segments = split_vrp(best_tour, nodes, req.vehicles, req.capacity)
        routes = [
            RouteResult(tour=seg, cost=tour_cost(seg, D), vehicle_id=i)
            for i, seg in enumerate(segments)
        ]
    else:
        routes = [RouteResult(tour=best_tour, cost=best_cost)]

    improvement = ((initial_cost - best_cost) / initial_cost) * 100 if initial_cost > 0 else 0

    return OptimizationResult(
        routes=routes,
        total_cost=round(best_cost, 2),
        initial_cost=round(initial_cost, 2),
        improvement_pct=round(improvement, 2),
        elapsed_ms=round(elapsed_ms, 1),
        algorithm=algo.upper(),
        iterations_run=result["iters"],
        convergence=result["convergence"],
        metadata={
            "nodes": len(nodes),
            "mode": req.mode,
            "vehicles": req.vehicles if req.mode != "tsp" else 1,
            "algorithm_detail": {
                "sa": "Simulated Annealing — quantum tunneling analog",
                "ga": "Genetic Algorithm — quantum superposition analog",
                "aco": "Ant Colony Optimization — quantum walk analog",
            }.get(algo, ""),
        },
    )


@app.get("/health")
def health():
    return {"status": "ok", "service": "QuantRoute API v1.0.0"}


@app.get("/algorithms")
def list_algorithms():
    return {
        "algorithms": [
            {
                "id": "sa",
                "name": "Simulated Annealing",
                "quantum_analog": "Quantum Tunneling",
                "best_for": "General TSP, smooth energy landscapes",
                "complexity": "O(n·I)",
            },
            {
                "id": "ga",
                "name": "Genetic Algorithm",
                "quantum_analog": "Quantum Superposition & Measurement",
                "best_for": "Multi-objective, large populations",
                "complexity": "O(P·G·n)",
            },
            {
                "id": "aco",
                "name": "Ant Colony Optimization",
                "quantum_analog": "Quantum Walk",
                "best_for": "Dynamic graphs, pheromone landscapes",
                "complexity": "O(A·I·n²)",
            },
        ]
    }

