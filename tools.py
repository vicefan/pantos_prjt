import networkx as nx
import json

def dijkstra(graph, start_node, end_node, priority_key):
    """
    개선된 다익스트라 알고리즘으로 최적 경로를 찾는 함수.
    동일한 우선순위 값을 가진 경로 중에서는 탄소 배출량이 낮은 경로를 선택합니다.
    """
    if start_node == end_node:
        return "Same node"
    
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
        return "No path found"
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

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
    
    # 노드 및 엣지 추가
    for from_node, destinations in graph.items():
        for to_node, edges in destinations.items():
            for i, edge in enumerate(edges):
                G.add_edge(
                    from_node, to_node, key=f"{from_node}-{to_node}-{i}", 
                    **edge
                )
    
    try:
        # 모든 단순 경로 찾기 (cutoff로 경로 길이 제한)
        all_paths = list(nx.all_simple_paths(G, source=start, target=end, cutoff=6))
        
        if not all_paths:
            return "no_path"
            
        # 각 경로에 대해 모든 가능한 엣지 조합을 고려하여 경로 상세 정보 생성
        path_details = []
        
        # 각 노드 경로에 대해
        for path_nodes in all_paths[:max_paths]:  # 너무 많은 경로는 제한
            # 각 인접 노드 쌍에 대해 가능한 엣지 조합 계산
            edge_options = []
            
            for i in range(len(path_nodes) - 1):
                from_node = path_nodes[i]
                to_node = path_nodes[i+1]
                
                # 두 노드 간의 모든 가능한 엣지
                edges = []
                for edge_id, edge_data in G[from_node][to_node].items():
                    edges.append(edge_data)
                
                edge_options.append(edges)
            
            # 각 경로의 첫 번째 엣지 옵션만 사용 (간략화)
            path_detail = {
                'nodes': path_nodes,
                'path_details': [],
                'time': 0,
                'cost': 0,
                'distance': 0,
                'carbon': 0,
                'transfers': len(path_nodes) - 2
            }
            
            # 경로 상세 정보 및 총 비용 계산
            for i in range(len(path_nodes) - 1):
                from_node = path_nodes[i]
                to_node = path_nodes[i+1]
                edge = edge_options[i][0]  # 첫 번째 엣지 옵션 사용
                
                path_detail['path_details'].append({
                    'from': from_node,
                    'to': to_node,
                    'mode': edge['mode'],
                    'time': edge['time'],
                    'cost': edge['cost'],
                    'carbon': edge['carbon']
                })
                
                path_detail['time'] += edge['time']
                path_detail['cost'] += edge['cost']
                path_detail['distance'] += edge['distance']
                path_detail['carbon'] += edge['carbon']
            
            path_details.append(path_detail)
        
        # 경로를 소요 시간 기준으로 정렬
        path_details.sort(key=lambda x: x['time'])
        
        return path_details
    
    except Exception as e:
        print(f"경로 탐색 중 오류 발생: {str(e)}")
        return None

def search_routes(graph, start, end, selected_priority):
    """경로 검색 로직"""
    # 우선순위 정의
    priorities = {
        '최소 시간순': 'time',
        '최소 비용순': 'cost',
        '최소 환적순': 'transfers'
    }
    
    # 시작 노드와 종료 노드가 같은 경우
    if start == end:
        return "same_node"
    
    # 모든 경로 찾기 옵션
    if selected_priority == '모든 경로':
        all_paths = find_all_paths(graph, start, end)
        if isinstance(all_paths, str) and all_paths == "no_path":
            return "no_path"
        return {"모든 가능한 경로": all_paths}
    else:
        # 선택된 우선순위에 대해서만 최적 경로 계산
        key = priorities[selected_priority]
        result = dijkstra(graph, start, end, key)
        
        if result == "No path found":
            return "no_path"
        elif result == "Same node":
            return "same_node"
        
        # 단일 경로 결과를 리스트로 감싸서 반환
        return {selected_priority: [result]}