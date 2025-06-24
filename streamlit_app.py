import streamlit as st
from streamlit_option_menu import option_menu
from get_spread_data import get_data

# 간단한 페이지 설정
st.set_page_config(
    page_title="Pantos Project",
    page_icon="🚢",
    layout="wide"
)

# --- CSS 스타일 정의 ---
with open("css_style.txt", "r") as f:
    css_style = f.read()
st.markdown(css_style, unsafe_allow_html=True)

# --- 제목 ---
st.markdown("<h1>예상 물류비 조회</h1>", unsafe_allow_html=True)
st.markdown("<hr style='border: none; height: 2px; background-color: #E3ECF7; margin: 20px 0;'>", unsafe_allow_html=True)

# --- 운송모드 ---
st.markdown("""
<div class="option-row">
    <span class="option-label">운송모드</span>
""", unsafe_allow_html=True)

selected_mode = option_menu(
    menu_title=None,
    options=["해운", "항공", "철도", "복합"],
    icons=['truck', 'airplane', 'train-front', 'box-seam'],
    default_index=0,
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

st.markdown("<hr style='border: none; height: 2px; background-color: #E3ECF7; margin: 20px 0;'>", unsafe_allow_html=True)

st.markdown("""
</div>
<div class="option-row">
    <span class="option-label">옵션</span>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns([1.5, 1.5, 1])

with col1:
    select_start = st.selectbox(
        label="출발지",
        options=["인천", "부산"],
        placeholder="출발지를 선택하세요.",
        index=None,
        key="start"
    )
with col2:
    select_listbox = st.selectbox(
        label="분류 기준",
        options=["최소 비용순", "최소 환적순"],
        placeholder="분류 기준을 선택하세요.",
        index=None,
        key="sort"
    )
with col3:
    st.markdown("<div style='height: 8px'></div>", unsafe_allow_html=True)  # 버튼 위 정렬용
    search_clicked = st.button("조회하기", use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# --- 결과 출력 ---
if search_clicked:
    if not select_start or not select_listbox:
        st.warning("출발지와 분류 기준을 모두 선택해 주세요.")
    else:
        data = get_data(select_start)
        if select_listbox == "최소 비용순":
            st.write("최소 비용순으로 정렬된 경로를 보여줍니다.")
            result = sorted(data, key=lambda x: (x['비용(USD/TEU)'], x["탄소배출량"]))
            st.dataframe(result, use_container_width=True)
        elif select_listbox == "최소 환적순":
            st.write("최소 환적순으로 정렬된 경로를 보여줍니다.")
            result = sorted(data, key=lambda x: (x['환적 횟수'], x["탄소배출량"]))
            st.dataframe(result, use_container_width=True)