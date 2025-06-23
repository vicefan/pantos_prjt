from get_spread_data import get_data
import streamlit as st

# 간단한 페이지 설정
st.set_page_config(
    page_title="Pantos Project",
    page_icon="🚢",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 제목 지정
st.title("예상 물류비 조회")

# 스프레드시트에서 데이터 가져오기
data = get_data()

# 비용순으로 볼건지 환적순으로 볼건지 선택하는 selectbox
select_listbox = st.selectbox(
    label="분류 기준",
    options=["최소 비용순", "최소 환적순"],
    placeholder="Choose option to sort the routes",
    index=None
)

# 위에 selectbox에서 선택한 값에 따라 데이터 정렬 및 출력
if select_listbox == "최소 비용순":
    st.write("최소 비용순으로 정렬된 경로를 보여줍니다.")
    result = sorted(data, key=lambda x: (x['비용(USD/TEU)'], x["탄소배출량"])) # 비용이 같으면 탄소배출량으로 정렬
    st.dataframe(result)
elif select_listbox == "최소 환적순":
    st.write("최소 환적순으로 정렬된 경로를 보여줍니다.")
    result = sorted(data, key=lambda x: (x['환적 횟수'], x["탄소배출량"])) # 환적 횟수가 같으면 탄소배출량으로 정렬
    st.dataframe(result)
    