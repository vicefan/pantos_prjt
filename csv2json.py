import csv
import json
from collections import defaultdict

def csv_to_graph_json(csv_path, json_path):
    graph = defaultdict(lambda: defaultdict(list))

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if not row or len(row) < 7:
                continue  # skip invalid rows
            from_node, to_node, mode, time, cost, distance, carbon = row
            edge = {
                "mode": mode,
                "time": str(time),
                "cost": str(cost),
                "distance": str(distance),
                "carbon": str(carbon)
            }
            graph[from_node][to_node].append(edge)

    # defaultdict을 일반 dict로 변환
    graph = {k: dict(v) for k, v in graph.items()}

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=4)

# 사용 예시
CSV_FILE = r'C:\Users\vicefan\vscode_project\pantos_prjt\csv_Example.csv'
JSON_FILE = r'C:\Users\vicefan\vscode_project\pantos_prjt\test.json'
csv_to_graph_json(CSV_FILE, JSON_FILE)