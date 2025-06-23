from get_spread_data import get_data
import streamlit as st

# test code
st.set_page_config(
    page_title="Pantos Project",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("예상 물류비 조회")

data = get_data()

select_listbox = st.selectbox(
    "분류 기준",
    options=["최소 비용순", "최소 환적순"],
    placeholder="Choose option to sort the routes",
    index=None
)

if select_listbox == "최소 비용순":
    st.write("최소 비용순으로 정렬된 경로를 보여줍니다.")
    result = sorted(data, key=lambda x: (x['비용(USD/TEU)'], x["탄소배출량"]))
    st.dataframe(result)
elif select_listbox == "최소 환적순":
    st.write("최소 환적순으로 정렬된 경로를 보여줍니다.")
    result = sorted(data, key=lambda x: (x['환적 횟수'], x["탄소배출량"]))
    st.dataframe(result)
    