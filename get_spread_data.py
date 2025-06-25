import pandas as pd
# 구글 스프레드시트에서 데이터를 가져오기 위한 라이브러리
from oauth2client.service_account import ServiceAccountCredentials
import gspread

# Streamlit 라이브러리
import streamlit as st


def get_data(start, end="로테르담"):
    # 구글 스프레드시트 인증 + 데이터 가져오는 링크
    scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']

    # Streamlit의 secrets에서 서비스 계정 키를 가져옴
    json_key = dict(st.secrets["gcp_service_account"])

    # ServiceAccountCredentials 객체 생성 for 로그인
    credential = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
    gc = gspread.authorize(credential)
    # 우리 스프레드시트 URL
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/12iMwBipGnwo7ufP_ASObQwz20xp_CBNrs8MAUKbQxdM/edit?usp=sharing"

    # 스프레드시트 열기
    doc = gc.open_by_url(spreadsheet_url)
    # 시트 선택
    sheet = doc.worksheet("csv_Example")

    # 시트의 모든 값을 가져와서 DataFrame으로 변환
    values = sheet.get_all_values()
    # 첫 번째 행을 열 이름으로 사용하고 나머지 행을 데이터로 사용
    df = pd.DataFrame(data=values[1:], columns=values[0])
    # 공백이나 False인 열 이름 제거
    df = df[[col for col in df.columns if col and not col.isspace()]]


    # df를 파이썬 dict 형태로 변환
    data_list = df.to_dict(orient='records')

    # 데이터 전처리
    for data in data_list:
        # 비용, 소요일, 거리는 정수로 변환
        # 탄소배출량은 실수로 변환
        data['비용(USD/TEU)'] = int(data['비용(USD/TEU)']) if data['비용(USD/TEU)'] else 0
        data['소요일'] = int(data['소요일']) if data['소요일'] else 0
        data['거리'] = int(data['거리']) if data['거리'] else 0
        data['탄소배출량'] = int(data['탄소배출량']) if data['탄소배출량'] else 0

        # 엣지 이름이 '직송'인 경우 환적 횟수 = 0, 엣지이름이랑 전체경로도 직송이므로 continue
        if data['엣지 이름'] == '직송':
            data['환적 횟수'] = 0
            continue

        # 엣지 이름이 '직송'이 아닌 경우 엣지 이름과 전체 경로 앞 뒤 공백 제거 (strip)
        data['엣지 이름'] = data['엣지 이름'].strip()
        data['전체 경로'] = data['전체 경로'].strip()

        # "-"를 기준으로 전체 경로를 분리하여 환적 횟수 계산
        data['환적 횟수'] = len(data['전체 경로'].split('-'))
    

    # 출발지가 인천이면 항공운송 모드가 포함된 데이터만 반환
    if start == "인천":
        tmp = [d for d in data_list if '항공운송' in d['모드']]
        for d in tmp:
            # 엣지 이름이 '직송'인 경우 전체 경로를 출발지와 도착지로 설정
            if d['엣지 이름'] == '직송':
                d['전체 경로'] = f"{start}-{end}"
                continue
            d['전체 경로'] = f"{start}-{d['전체 경로']}-{end}"
        return tmp
    else:
        # 출발지가 부산이면 항공운송 모드가 포함되지 않은 데이터만 반환
        tmp = [d for d in data_list if '항공운송' not in d['모드']]
        for d in tmp:
            # 엣지 이름이 '직송'인 경우 전체 경로를 출발지와 도착지로 설정
            if d['엣지 이름'] == '직송':
                d['전체 경로'] = f"{start}-{end}"
                continue
            d['전체 경로'] = f"{start}-{d['전체 경로']}-{end}"
        return tmp