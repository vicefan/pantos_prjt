from tools import dijkstra, load_graph, find_all_paths
import streamlit as st

# 페이지 설정
st.set_page_config(
    page_title="Pantos Project",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

def search_routes(graph, start, end, selected_priority):
    """경로 검색 로직"""
    # 우선순위 정의
    priorities = {
        '최소 시간순': 'time',
        '최소 비용순': 'cost',
        '최소 환적순': 'transfers'
    }
    
    # 결과 컨테이너 초기화
    results = {}
    
    # 선택된 우선순위만 처리
    if selected_priority == '모든 경로':
        all_paths = find_all_paths(graph, start, end)
        if all_paths == "no_path":
            return "no_path"
        return {"모든 가능한 경로": all_paths}
    else:
        # 선택된 우선순위에 대해서만 경로 계산
        key = priorities[selected_priority]
        result = dijkstra(graph, start, end, key)
        if result == "No path found":
            return "no_path"
        elif result == "Same node":
            return "same_node"
        results[selected_priority] = result
    
    return results

def main():
    """Streamlit 앱 메인 함수"""
    st.title("🌎 LXP")
    
    # 그래프 데이터 로드
    graph = load_graph()
    nodes = list(graph.keys())
    
    # 사이드바: 입력 컨트롤 
    with st.sidebar:
        st.header("경로 검색 설정")
        
        # 출발지 및 도착지 선택
        start = st.selectbox(
            "출발지 선택",
            nodes,
            index=0,
            key="start_node"
        )
        
        end = st.selectbox(
            "도착지 선택", 
            nodes,
            index=len(nodes)-1,
            key="end_node"
        )
        
        # 우선순위 선택
        priority_options = ["모든 경로", "최소 시간순", "최소 비용순", "최소 환적순"]
        selected_priority = st.selectbox(
            "우선순위 선택",
            priority_options,
            index=0,
            key="priority"
        )
        
        # 검색 버튼
        search_clicked = st.button("🔍 경로 검색", type="primary")
        
        st.divider()
        st.write("### 정보")
        st.info("출발지와 도착지를 선택한 후 '경로 검색' 버튼을 클릭하세요.")
        st.success("모든 경로는 동일 조건에서 탄소 배출량이 낮은 경로가 우선 선택됩니다.")
        
        # 그래프 정보 표시
        with st.expander("데이터 정보"):
            st.write(f"- 노드 수: {len(nodes)}")
            edge_count = sum(len(dest) for node in graph.values() for dest in node.values())
            st.write(f"- 엣지 수: {edge_count}")
    
    # 경로 검색 실행
    if search_clicked:
        st.toast(f"경로 검색 중: {start} → {end}")
        
        # 경로 검색 실행
        results = search_routes(graph, start, end, selected_priority)
        
        # 결과 처리
        if results == "no_path":
            st.error(f"💔 {start}에서 {end}까지 경로를 찾을 수 없습니다.")
        elif results == "same_node":
            st.warning("⚠️ 출발지와 도착지가 동일합니다.")
        else:
            # 결과 표시 영역
            st.header(f"🚢 {start} → {end} 경로 검색 결과")
            
            # 각 우선순위별 결과 표시
            for name, data in results.items():
                print(data)
                days = data['time'] / 24
                
                with st.expander(f"⭐ {name}", expanded=True):
                    # 경로 정보
                    path_str = " → ".join([p['to'] for p in data['path_details']])
                    full_path = f"{data['path_details'][0]['from']} → {path_str}"
                    
                    # 경로 정보를 표로 정리
                    st.markdown(f"**전체 경로**: {full_path}")
                    
                    # 요약 정보를 열로 표시
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("총 소요 시간", f"{days:.1f}일 ({data['time']}시간)")
                    with col2:
                        st.metric("총 비용", f"${data['cost']:,}")
                    with col3:
                        st.metric("환적 횟수", f"{data['transfers']}회")
                    
                    # 탄소 배출량
                    st.metric("총 탄소 배출량", f"{data['carbon']:,} kg CO2e")
                    
                    # 구간별 상세 정보
                    st.subheader("구간별 상세 정보")
                    
                    # 데이터 테이블로 변환
                    table_data = []
                    for segment in data['path_details']:
                        table_data.append({
                            "출발": segment['from'],
                            "도착": segment['to'],
                            "운송 수단": segment['mode'],
                            "소요 시간(시간)": segment['time'],
                            "비용($)": f"${segment['cost']:,}"
                        })
                    
                    # 테이블 표시
                    st.table(table_data)
    else:
        # 검색 전 초기 화면
        st.markdown("""
        이 애플리케이션은 국제 물류 운송 경로를 보여줍니다.
        
        **사용 방법:**
        1. 왼쪽 사이드바에서 출발지와 도착지를 선택하세요
        2. 우선순위 기준을 선택하세요 (시간, 비용, 탄소배출, 환적횟수)
        3. '경로 검색' 버튼을 클릭하세요
        
        **경로 우선순위 설명:**
        - **최소 시간순**: 가장 빠른 경로
        - **최소 비용순**: 가장 저렴한 경로
        - **최소 환적순**: 환적 횟수가 적은 경로
                    
        **참고**: 모든 경로는 동일한 조건에서 탄소 배출량이 낮은 경로가 우선적으로 선택됩니다.
        
        왼쪽 사이드바에서 시작하세요!
        """)
        
        # 샘플 이미지 또는 아이콘 표시
        st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=300)

if __name__ == '__main__':
    main()