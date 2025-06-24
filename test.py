import streamlit as st
from streamlit_option_menu import option_menu
from get_spread_data import get_data

st.set_page_config(layout="wide")

# --- CSS 스타일 정의 ---
st.markdown("""
<style>
.block-container {
    max-width: 900px !important;
    margin: 40px auto 40px auto;
    padding: 32px 24px;
    background: #F5F7FA;
    border-radius: 16px;
    box-shadow: 0 4px 12px rgba(25, 118, 210, 0.06);
}
h1 {
    color: #1976D2;
    font-weight: 700;
    text-align: center;
}
.stSelectbox > div > div {
    background: #fff !important;
    border-radius: 8px !important;
    border: 1px solid #E3ECF7 !important;
}
.stButton > button {
    background-color: #1976D2 !important;
    color: #fff !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    padding: 0.5em 2em !important;
    margin-left: 10px;
}
.option-row {
    display: flex;
    align-items: center;
    gap: 18px;
    margin-bottom: 24px;
    margin-top: 24px;
}
.option-label {
    font-weight: bold;
    font-size: 16px;
    color: #555;
    margin-right: 10px;
    min-width: 48px;
}
</style>
""", unsafe_allow_html=True)

# --- 제목 ---
st.markdown("<h1>예상 물류비 조회</h1>", unsafe_allow_html=True)

# --- 운송모드 + 옵션 한 줄 배치 ---
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
        "container": {"padding": "0!important", "background-color": "#F5F7FA", "display": "inline-block"},
        "icon": {"color": "#1976D2", "font-size": "20px"},
        "nav": {"gap": "10px"},
        "nav-link": {
            "font-size": "16px",
            "text-align": "center",
            "padding": "16px 18px",
            "margin": "0px",
            "border": "1px solid #E3ECF7",
            "border-radius": "8px",
            "color": "#1976D2",
            "--hover-color": "#E3ECF7"
        },
        "nav-link-selected": {
            "background-color": "#1976D2",
            "color": "#fff",
            "border": "1px solid #1976D2",
            "font-weight": "bold",
        },
        "nav-link-selected > span": {
            "color": "#fff",
        }
    }
)

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