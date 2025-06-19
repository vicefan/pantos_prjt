import networkx as nx
import json
import itertools

def dijkstra(graph, start_node, end_node, priority_key):
    """
    개선된 다익스트라 알고리즘으로 최적 경로를 찾는 함수.
    동일한 우선순위 값을 가진 경로 중에서는 탄소 배출량이 낮은 경로를 선택합니다.
    """
    if start_node == end_node:
        return "same_node"
    
    G = nx.MultiDiGraph()
    
    # 노드 및 엣지 추가 - 가중치에 탄소 배출량을 2차 기준으로 포함
    for from_node, destinations in graph.items():
        for to_node, edges in destinations.items():
            for edge in edges:
                # 우선순위에 따른 가중치 설정
                primary_weight = 1 if priority_key == 'transfers' else edge[priority_key]
                
                # 간선 추가 (모든 정보 저장)
                G.add_edge(from_node, to_node, 
                          weight=primary_weight,
                          carbon_weight=edge['carbon'],
                          mode=edge['mode'],
                          time=edge['time'],
                          cost=edge['cost'],
                          distance=edge['distance'],
                          carbon=edge['carbon'])
    
    try:
        # 다익스트라 알고리즘으로 최단 경로 찾기
        path_nodes = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
        
        result = {
            'time': 0,
            'cost': 0,
            'distance': 0,
            'carbon': 0,
            'transfers': len(path_nodes) - 2,
            'path_details': []
        }
        
        # 경로 상세 정보 생성
        for i in range(len(path_nodes) - 1):
            from_node = path_nodes[i]
            to_node = path_nodes[i+1]
            
            # 동일 가중치의 간선이 여러 개인 경우, 탄소 배출량이 낮은 것 선택
            min_weight = float('inf')
            min_carbon = float('inf')
            best_edge = None
            
            for edge_id, edge_data in G[from_node][to_node].items():
                current_weight = edge_data['weight']
                carbon_weight = edge_data['carbon_weight']
                
                # 더 작은 가중치를 가진 간선 선택
                if current_weight < min_weight:
                    min_weight = current_weight
                    min_carbon = carbon_weight
                    best_edge = edge_data
                # 가중치가 같으면 탄소 배출량이 더 적은 간선 선택
                elif current_weight == min_weight and carbon_weight < min_carbon:
                    min_carbon = carbon_weight
                    best_edge = edge_data
            
            # 최적 간선 정보 누적
            result['time'] += best_edge['time']
            result['cost'] += best_edge['cost']
            result['distance'] += best_edge['distance']
            result['carbon'] += best_edge['carbon']
            
            # 경로 상세 정보 추가
            result['path_details'].append({
                "from": from_node,
                "to": to_node,
                "mode": best_edge['mode'],
                "time": best_edge['time'],
                "cost": best_edge['cost'],
                "carbon": best_edge['carbon']
            })
        
        return result
    
    except nx.NetworkXNoPath:
        return "no_path"
    except Exception as e:
        print(f"다익스트라 알고리즘 오류: {e}")
        return "error"  # 문제 발생 시 명확한 문자열 반환

def load_graph():
    """JSON 파일에서 그래프 데이터 로드"""
    try:
        with open('graph.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        # 샘플 그래프 제공
        return {
            "Incheon": {
                "Shanghai": [
                    {"mode": "Sea", "time": 48, "cost": 300, "distance": 850, "carbon": 500},
                    {"mode": "Air", "time": 2, "cost": 1500, "distance": 850, "carbon": 4000}
                ],
                "Vladivostok": [
                    {"mode": "Sea", "time": 72, "cost": 400, "distance": 1000, "carbon": 600}
                ]
            },
            "Shanghai": {
                "Duisburg": [
                    {"mode": "Rail", "time": 360, "cost": 2000, "distance": 9000, "carbon": 3000}
                ]
            },
            "Vladivostok": {
                "Duisburg": [
                    {"mode": "Rail", "time": 240, "cost": 1800, "distance": 10000, "carbon": 2500}
                ]
            },
            "Duisburg": {
                "Warsaw": [
                    {"mode": "Rail", "time": 24, "cost": 200, "distance": 1000, "carbon": 150},
                    {"mode": "Truck", "time": 18, "cost": 300, "distance": 1000, "carbon": 250}
                ]
            },
            "Warsaw": {}
        }

def find_all_paths(graph, start, end, max_paths=10):
    """
    NetworkX를 사용하여 시작 노드에서 종료 노드까지의 모든 단순 경로를 찾는 함수
    """
    G = nx.MultiDiGraph()
    for from_node, destinations in graph.items():
        for to_node, edges in destinations.items():
            for edge in edges:
                G.add_edge(from_node, to_node, **edge)

    try:
        all_node_paths = list(nx.all_simple_paths(G, source=start, target=end, cutoff=6))
        if not all_node_paths:
            return "no_path"

        path_details = []
        seen = set()
        for node_path in all_node_paths:
            edge_options = []
            for i in range(len(node_path) - 1):
                from_node = node_path[i]
                to_node = node_path[i+1]
                options = []
                for key, edge in G[from_node][to_node].items():
                    options.append(edge)
                edge_options.append(options)
            for combo in itertools.product(*edge_options):
                combo_key = (
                    tuple(node_path),
                    tuple(edge['mode'] for edge in combo)
                )
                if combo_key in seen:
                    continue
                seen.add(combo_key)
                total_time = sum(edge['time'] for edge in combo)
                total_cost = sum(edge['cost'] for edge in combo)
                total_distance = sum(edge['distance'] for edge in combo)
                total_carbon = sum(edge['carbon'] for edge in combo)
                transfers = len(node_path) - 2
                path_details.append({
                    'nodes': node_path,
                    'time': total_time,
                    'cost': total_cost,
                    'distance': total_distance,
                    'carbon': total_carbon,
                    'transfers': transfers,
                    'path_details': [
                        {
                            'from': node_path[i],
                            'to': node_path[i+1],
                            'mode': combo[i]['mode'],
                            'time': combo[i]['time'],
                            'cost': combo[i]['cost'],
                            'distance': combo[i]['distance'],
                            'carbon': combo[i]['carbon'],
                        }
                        for i in range(len(combo))
                    ]
                })
        path_details.sort(key=lambda x: x['time'])
        return path_details[:max_paths] if max_paths else path_details

    except Exception as e:
        print(f"경로 탐색 중 오류 발생: {str(e)}")
        return None