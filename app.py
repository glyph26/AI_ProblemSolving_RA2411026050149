from flask import Flask, render_template, request
import itertools
import time

app = Flask(__name__)

# -----------------------------
# Algorithms
# -----------------------------
def brute_force_tsp(dist):
    n = len(dist)
    best_cost = float('inf')
    best_path = None

    for perm in itertools.permutations(range(1, n)):
        path = [0] + list(perm) + [0]
        cost = sum(dist[path[i]][path[i+1]] for i in range(len(path)-1))

        if cost < best_cost:
            best_cost = cost
            best_path = path

    return best_path, best_cost


def nearest_neighbor_tsp(dist):
    n = len(dist)
    visited = [False]*n
    path = [0]
    visited[0] = True
    cost = 0
    current = 0

    for _ in range(n-1):
        next_city = min(
            [(dist[current][j], j) for j in range(n) if not visited[j]]
        )[1]

        cost += dist[current][next_city]
        path.append(next_city)
        visited[next_city] = True
        current = next_city

    cost += dist[current][0]
    path.append(0)

    return path, cost


# -----------------------------
# Route
# -----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    result = None

    if request.method == "POST":
        size = int(request.form["size"])
        dist = []

        for i in range(size):
            row = []
            for j in range(size):
                val = int(request.form.get(f"cell_{i}_{j}", 0))
                row.append(val)
            dist.append(row)

        # High precision timing
        start = time.perf_counter()
        bf_path, bf_cost = brute_force_tsp(dist)
        bf_time = time.perf_counter() - start

        start = time.perf_counter()
        nn_path, nn_cost = nearest_neighbor_tsp(dist)
        nn_time = time.perf_counter() - start

        result = {
            "bf_path": bf_path,
            "bf_cost": bf_cost,
            "bf_time": f"{bf_time:.8f}",
            "nn_path": nn_path,
            "nn_cost": nn_cost,
            "nn_time": f"{nn_time:.8f}"
        }

    return render_template("index.html", result=result)


if __name__ == "__main__":
    app.run(debug=True)