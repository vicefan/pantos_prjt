import streamlit as st
from streamlit_option_menu import option_menu
# get_spread_data.py에서 get_data 함수를 가져옴
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
col1, col2, col3 = st.columns([1.5, 1.5, 1]) # 숫자는 각각의 너비 비율

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
# 분류 기준 column
with col2:
    # 분류 기준 선택 박스
    select_listbox = st.selectbox(
        label="분류 기준",
        options=["최소 비용순", "최소 환적순"],
        placeholder="분류 기준을 선택하세요.",
        index=None,
        key="sort"
    )
# 조회하기 버튼 column
with col3:
    # 조회하기 버튼
    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)
    search_clicked = st.button("조회하기", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

if search_clicked: # 조회하기 버튼 클릭 시 동작
    # 출발지와 분류 기준이 모두 선택되었는지 확인
    # 만약 둘 중 하나라도 선택되지 않았다면 경고 메시지 출력
    if not select_start or not select_listbox:
        st.warning("출발지와 분류 기준을 모두 선택해 주세요.")
    # 둘 다 선택되었다면 get_data 함수를 호출(/출발지/를 파라미터로 사용)하여 데이터를 가져옴
    else:
        data = get_data(select_start)
        if select_listbox == "최소 비용순":
            st.write("최소 비용순으로 정렬된 경로를 보여줍니다.")
            # 비용 순 정렬 후 탄소 배출량 순 정렬
            result = sorted(data, key=lambda x: (x['비용(USD/TEU)'], x["탄소배출량"]))
            st.dataframe(result, use_container_width=True)
        elif select_listbox == "최소 환적순":
            st.write("최소 환적순으로 정렬된 경로를 보여줍니다.")
            # 환적 횟수 순 정렬 후 탄소 배출량 순 정렬
            result = sorted(data, key=lambda x: (x['환적 횟수'], x["탄소배출량"]))
            st.dataframe(result, use_container_width=True)