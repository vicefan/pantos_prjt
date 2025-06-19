import networkx as nx 

def dijkstra(graph, start_node, end_node, priority_key):
    """
    NetworkX를 사용하여 다익스트라 알고리즘으로 최적 경로를 찾는 함수.
    """
    if start_node == end_node:
        return "Same node"
    
    G = nx.MultiDiGraph()
    
    # 노드 및 엣지 추가
    for from_node, destinations in graph.items():
        for to_node, edges in destinations.items():
            for edge in edges:
                # transfers인 경우는 모든 간선 가중치를 1로 설정 (노드 방문 횟수 최소화)
                weight = 1 if priority_key == 'transfers' else edge[priority_key]
                
                # 간선 추가 (모든 정보 저장)
                G.add_edge(from_node, to_node, 
                          weight=weight,
                          mode=edge['mode'],
                          time=edge['time'],
                          cost=edge['cost'],
                          distance=edge['distance'],
                          carbon=edge['carbon'])
    
    try:
        path_nodes = nx.dijkstra_path( # nx.bellman_ford_path, nx.astar_path, and more
            G, 
            source=start_node, 
            target=end_node, 
            weight='weight')
    except nx.NetworkXNoPath:
        return "No path found"
    
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
        
        # 멀티그래프에서는 두 노드 사이에 여러 간선 중 가중치가 최소인 것 선택
        min_weight = float('inf')
        best_edge = None
        
        for edge_id, edge_data in G[from_node][to_node].items():
            if edge_data['weight'] < min_weight:
                min_weight = edge_data['weight']
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
            "cost": best_edge['cost']
        })
    
    return result

