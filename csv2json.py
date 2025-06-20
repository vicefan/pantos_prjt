import csv
import json
from collections import defaultdict

def c2j(csv_path, json_path):
    graph = defaultdict(lambda: defaultdict(list))

    with open(csv_path, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
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

    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(graph, f, ensure_ascii=False, indent=4)



# 여기 아래에 csv 파일 경로랑 json 파일 경로 쓰면 같은 폴더 내에 test.json 파일로 저장됨
CSV_FILE = r'.\csv_Example.csv'
JSON_FILE = r'.\test.json'
c2j(CSV_FILE, JSON_FILE)