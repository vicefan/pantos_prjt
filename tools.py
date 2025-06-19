import networkx as nx 

def dijkstra(graph, start_node, end_node, priority_key):
    """
    개선된 다익스트라 알고리즘으로 최적 경로를 찾는 함수.
    동일한 우선순위 값을 가진 경로 중에서는 탄소 배출량이 낮은 경로를 선택합니다.
    """
    if start_node == end_node:
        return "Same node"
    
    G = nx.MultiDiGraph()
    
    # 노드 및 엣지 추가 - 가중치 튜플로 설정 (주 우선순위, 탄소 배출량)
    for from_node, destinations in graph.items():
        for to_node, edges in destinations.items():
            for edge in edges:
                # 우선순위 키에 따른 가중치 설정
                if priority_key == 'transfers':
                    main_weight = 1  # 환적 횟수는 간선당 1로 고정
                else:
                    main_weight = edge[priority_key]
                    
                # 동일 우선순위일 때 탄소 배출량으로 두 번째 기준 설정
                carbon_weight = edge['carbon']
                
                # 간선 추가 (모든 정보 저장)
                G.add_edge(from_node, to_node, 
                          weight=main_weight,  # 주 가중치
                          carbon=carbon_weight,  # 부 가중치 (동점 처리용)
                          mode=edge['mode'],
                          time=edge['time'],
                          cost=edge['cost'],
                          distance=edge['distance'])
    
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
                # 주 우선순위가 더 낮은 간선 선택
                if edge_data['weight'] < min_weight:
                    min_weight = edge_data['weight']
                    min_carbon = edge_data['carbon']
                    best_edge = edge_data
                # 주 우선순위가 같다면 탄소 배출량이 더 낮은 간선 선택
                elif edge_data['weight'] == min_weight and edge_data['carbon'] < min_carbon:
                    min_carbon = edge_data['carbon']
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