import streamlit as st
from streamlit_option_menu import option_menu
# 폴더 내 get_spread_data.py에서 get_data 함수를 가져옴
from get_spread_data import get_data


# 페이지 제목, 아이콘 설정 및 [wide, centered] 중 택 1
st.set_page_config(
    page_title="Pantos Project",
    page_icon="🚢",
    layout="wide"
)

# CSS 스타일 설정
with open("css_style.txt", "r") as f:
    css_style = f.read()
# st.markdown 을 사용하여 CSS 스타일 적용
st.markdown(css_style, unsafe_allow_html=True)

# 제목과 그 아래 구분선
st.markdown("<h1>예상 물류비 조회</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: none; height: 2px; background-color: #E3ECF7; margin: 20px 0;'>", unsafe_allow_html=True)


# 운송모드 글자
st.markdown("""
<div class="option-row">
    <span class="option-label">운송모드</span>
""", unsafe_allow_html=True)

# 운송모드 선택 버튼?
selected_mode = option_menu(
    menu_title=None,
    options=["해운", "항공", "철도", "복합"],
    icons=['truck', 'airplane', 'train-front', 'box-seam'],
    orientation="horizontal",
    styles={
        "container": {"background-color": "#F5F7FA"},
        "icon": {"font-size": "20px"},
        "nav": {"gap": "10px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "padding": "16px 18px",
            "margin": "5px",
            "border": "1px solid #E3ECF7",
            "border-radius": "8px"
        },
        
    }
)

# 구분선
st.markdown("<hr style='border: none; height: 2px; background-color: #E3ECF7; margin: 20px 0;'>", unsafe_allow_html=True)

# 옵션 글자
st.markdown("""
</div>
<div class="option-row">
    <span class="option-label">옵션</span>
""", unsafe_allow_html=True)

# 출발지 | 분류 기준 | 조회하기 버튼
col1, col2, col3, col4 = st.columns([1.5, 1.5 ,1.5, 1]) # 숫자는 각각의 너비 비율

# 출발지 column
with col1:
    # 출발지 선택 박스
    select_start = st.selectbox(
        label="출발지",
        options=["인천", "부산"],
        placeholder="출발지를 선택하세요.",
        index=None,
        key="start"
    )
with col2:
    # 출발지 선택 박스
    select_end = st.selectbox(
        label="도착지",
        options=["로테르담"],
        index=0
    )
# 분류 기준 column
with col3:
    # 분류 기준 선택 박스
    select_listbox = st.selectbox(
        label="분류 기준",
        options=["최소 비용순", "최단 거리순" ,"최소 환적순"],
        placeholder="분류 기준을 선택하세요.",
        index=None,
        key="sort"
    )
# 조회하기 버튼 column
with col4:
    # 조회하기 버튼
    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
    search_clicked = st.button("조회하기", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if search_clicked: # 조회하기 버튼 클릭 시 동작
    # 출발지, 분류 기준, 운송모드가 모두 선택되었는지 확인
    if not select_start or not select_listbox or not selected_mode:
        bool_dict = {"출발지": select_start, "분류 기준": select_listbox, "운송모드": selected_mode}
        # 선택되지 않은 항목들을 찾아서 경고 메시지 출력
        not_selected = [k for k, v in bool_dict.items() if not v]
        st.warning(f"다음 항목을 선택해주세요: {', '.join(not_selected)}")
    # 다 선택되었다면 get_data 함수를 호출(/출발지/를 파라미터로 사용)하여 데이터를 가져옴
    else:
        data = get_data(select_start, select_end)
        # 운송모드 필터링
        if selected_mode == "복합":
            data = [d for d in data if '+' in d['모드']]
        else:
            processed_mode = {
                "해운": "해상운송",
                "항공": "항공운송",
                "철도": "철도운송"
            }
            data = [d for d in data if processed_mode[selected_mode] in d['모드']]

        # 정렬
        if select_listbox == "최소 비용순":
            result = sorted(data, key=lambda x: (x['비용(USD/TEU)'], x["탄소배출량"]))
            st.markdown('<div style="font-size:15px; color:#888; margin-bottom:8px;">최소 비용순으로 정렬된 경로</div>', unsafe_allow_html=True)
        elif select_listbox == "최단 거리순":
            result = sorted(data, key=lambda x: (x['거리'], x['비용(USD/TEU)'], x["탄소배출량"]))
            st.markdown('<div style="font-size:15px; color:#888; margin-bottom:8px;">최단 거리순으로 정렬된 경로</div>', unsafe_allow_html=True)
        elif select_listbox == "최소 환적순":
            result = sorted(data, key=lambda x: (x['환적 횟수'], x['비용(USD/TEU)'], x["탄소배출량"]))
            st.markdown('<div style="font-size:15px; color:#888; margin-bottom:8px;">최소 환적순으로 정렬된 경로</div>', unsafe_allow_html=True)

        # 카드형 결과 출력
        card_html = ""
        for row in result:
            card_html += f"""
            <div style="border-radius: 16px; box-shadow: 0 2px 8px rgba(25, 118, 210, 0.06); border: 1.5px solid #f5eaea; margin-bottom: 24px; overflow: hidden;">
                <!-- 상단 경로(핑크) -->
                <div style="background: #fff6f4; padding: 22px 32px 18px 32px;">
                    <span style="display:inline-flex; align-items:center; background:#fff; border-radius: 999px; padding:10px 22px; font-size:18px; font-weight:600; color:#1976D2; box-shadow:0 1px 4px #eee;">
                        {row['전체 경로'].replace('-', '<span style="margin: 0 12px; color:#888;">&#8594;</span>')}
                    </span>
                </div>
                <!-- 하단 정보(흰색) -->
                <div style="background: #fff; padding: 22px 32px 18px 32px; display: flex; align-items: center; gap: 32px;">
                    <div style="flex:1;">
                        <b>예상 운임</b><br>
                        <span style="font-size:20px; color:#222;">$ {row['비용(USD/TEU)']:,}</span>
                    </div>
                    <div style="flex:1;">
                        <b>소요일</b><br>
                        <span style="font-size:20px; color:#1976D2;">{row['소요일']}</span>
                    </div>
                    <div style="flex:1;">
                        <b>환적 횟수</b><br>
                        <span style="font-size:20px; color:#1976D2;">{row['환적 횟수']}</span>
                    </div>
                    <div style="flex:1;">
                        <b>탄소 배출량</b><br>
                        <span style="font-size:20px; color:#1976D2;">{row['탄소배출량']}</span>
                    </div>
                </div>
            </div>
            """

        st.markdown(card_html, unsafe_allow_html=True)