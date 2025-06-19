from tools import load_graph, find_all_paths
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
    priorities = {
        '최소 시간순': 'time',
        '최소 비용순': 'cost',
        '최소 환적순': 'transfers'
    }
    if selected_priority == '모든 경로':
        all_paths = find_all_paths(graph, start, end)
        if all_paths == "no_path":
            return "no_path"
        return {"모든 가능한 경로": all_paths}
    else:
        all_paths = find_all_paths(graph, start, end)
        if all_paths == "no_path":
            return "no_path"
        key = priorities[selected_priority]
        # 모든 기준에 대해 2차 정렬로 carbon 추가
        sorted_paths = sorted(all_paths, key=lambda x: (x[key], x['carbon']))
        return {selected_priority: sorted_paths}

# Streamlit 앱 메인 함수 부분 수정
def main():
    """Streamlit 앱 메인 함수"""
    # 왼쪽 사이드바에 입력 컨트롤
    with st.sidebar:
        st.header("검색 설정")
        
        # 그래프 데이터 로드
        graph = load_graph()
        nodes = list(graph.keys())
        
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
        
        # 우선순위 선택 (탄소 배출순 제거)
        priority_options = ["모든 경로", "최소 시간순", "최소 비용순", "최소 환적순"]
        selected_priority = st.selectbox(
            "우선순위 선택",
            priority_options,
            index=0,
            key="priority"
        )
        
        # 정보 메시지
        if selected_priority != "모든 경로":
            st.info("💡 동일한 우선순위의 경로가 여러 개인 경우, 탄소 배출량이 낮은 순으로 정렬 됩니다.")
        
        # 검색 버튼
        search_clicked = st.button("🔍 경로 검색", type="primary", use_container_width=True)
        
        st.divider()
        st.write("### 정보")
        st.info("출발지와 도착지를 선택한 후 '경로 검색' 버튼을 클릭하세요.")
        
        # 그래프 정보 표시
        with st.expander("데이터 정보"):
            st.write(f"- 노드 수: {len(nodes)}")
            edge_count = sum(len(dest) for node in graph.values() for dest in node.values())
            st.write(f"- 엣지 수: {edge_count}")
    
    # 메인 영역
    # 경로 검색 실행
    if 'search_clicked' not in st.session_state:
        st.session_state.search_clicked = False
    
    if search_clicked or st.session_state.search_clicked:
        st.session_state.search_clicked = True
        
        # 경로 검색 실행
        results = search_routes(graph, start, end, selected_priority)

        # 결과 처리
        if results == "no_path" or results == "No path found":  # 대소문자 통일
            st.error(f"💔 {start}에서 {end}까지 경로를 찾을 수 없습니다.")
        elif results == "same_node" or results == "Same node":
            st.warning("⚠️ 출발지와 도착지가 동일합니다.")
        else:
            # 결과 표시 영역
            st.header(f"🚢 {start} → {end} 경로 검색 결과")
            
            # 각 우선순위별 결과 표시
            for name, paths in results.items():
                with st.expander(f"⭐ {name}", expanded=True):
                    if not paths:
                        st.warning("가능한 경로가 없습니다.")
                    else:
                        for idx, path in enumerate(paths):
                            nodes_str = " → ".join(path['nodes']) if 'nodes' in path else ""
                            modes_str = " → ".join([p['mode'] for p in path['path_details']]) if 'path_details' in path else ""
                            days = path['time'] / 24 if 'time' in path else 0

                            with st.expander(f"경로 {idx+1}: {nodes_str}", expanded=False):
                                st.write(f"**운송 수단:** {modes_str}")
                                st.write(f"**소요 시간:** {days:.1f}일 ({path['time']}시간)")
                                st.write(f"**비용:** ${path['cost']:,}")
                                st.write(f"**탄소 배출량:** {path['carbon']:,} kg")
                                st.write(f"**환적 횟수:** {path['transfers']}")
                                # 필요하다면 상세 경로 정보 등 추가
    else:
        # 검색 전 초기 화면
        st.markdown("""
        **사용 방법:**
        1. 왼쪽 사이드바에서 출발지와 도착지를 선택하세요
        2. 우선순위 기준을 선택하세요:
           - **모든 경로**: 가능한 모든 경로를 표시
           - **최소 시간순**: 가장 빠른 경로
           - **최소 비용순**: 가장 저렴한 경로
           - **최소 환적순**: 환적 횟수가 적은 경로
        3. '경로 검색' 버튼을 클릭하세요
        
        💡 동일한 우선순위 값을 가진 경로가 여러 개인 경우, 탄소 배출량이 가장 낮은 경로가 자동으로 선택됩니다.
        """)
        
        # 샘플 이미지 (이미지 로드에 문제가 있으면 이 부분 주석 처리)
        try:
            st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=300)
        except:
            st.write("이미지를 로드할 수 없습니다.")

if __name__ == '__main__':
    main()