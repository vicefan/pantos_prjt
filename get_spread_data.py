import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import streamlit as st

def get_data():
    scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']

    json_key = dict(st.secrets["gcp_service_account"])

    credential = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
    gc = gspread.authorize(credential)
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/12iMwBipGnwo7ufP_ASObQwz20xp_CBNrs8MAUKbQxdM/edit?usp=sharing"
    doc = gc.open_by_url(spreadsheet_url)
    sheet = doc.worksheet("csv_Example")

    values = sheet.get_all_values(pad_values=True)
    df = pd.DataFrame(data=values[1:], columns=values[0])
    df = df[df[df.columns[0]].notnull() and df[df.columns[0]] != '']

    result = df[df['엣지 이름'].str.endswith('경유')]

    data_list = result.to_dict(orient='records')
    for data in data_list:
        data['비용(USD/TEU)'] = int(data['비용(USD/TEU)']) if data['비용(USD/TEU)'] else 0
        data['소요일'] = int(data['소요일']) if data['소요일'] else 0
        data['엣지 이름'] = data['엣지 이름'].strip() 
        data['전체 경로'] = data['전체 경로'].strip() 
        data['환적 횟수'] = len(data['전체 경로'].split('-'))
        data['거리'] = int(data['거리']) if data['거리'] else 0
        data['탄소배출량'] = float(data['탄소배출량']) if data['탄소배출량'] else 0
    
    return data_list