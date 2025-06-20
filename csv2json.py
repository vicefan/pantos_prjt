import csv
import json
from collections import defaultdict
from make_csv import make_csv

def c2j():
    graph = defaultdict(lambda: defaultdict(list))
    reader = csv.reader(csvfile=make_csv())
    for row in reader:
        if not row or len(row) < 7:
            continue
        from_node, to_node, mode, time, cost, distance, carbon = row
        edge = {
            "mode": mode,
            "time": time,
            "cost": cost,
            "distance": distance,
            "carbon": carbon
        }
        graph[from_node][to_node].append(edge)

    graph = {k: dict(v) for k, v in graph.items()}

    return graph