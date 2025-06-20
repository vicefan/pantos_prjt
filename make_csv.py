import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import streamlit as st

def make_csv():
    scope = ['https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive']

    json_key = dict(st.secrets["gcp_service_account"])

    credential = ServiceAccountCredentials.from_json_keyfile_dict(json_key, scope)
    gc = gspread.authorize(credential)
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/12iMwBipGnwo7ufP_ASObQwz20xp_CBNrs8MAUKbQxdM/edit?usp=sharing"
    doc = gc.open_by_url(spreadsheet_url)
    sheet = doc.worksheet("csv_Example")


    df = pd.DataFrame(sheet.get_all_values())
    df.rename(columns=df.iloc[0], inplace = True)
    df.drop(df.index[0], inplace=True)

    data_list = df.to_csv(index=False)
    return data_list