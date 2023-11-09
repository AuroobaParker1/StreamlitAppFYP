import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Authenticate with Google Drive
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

# Open the Google Sheet
try:
    sheet = gc.open('StreamlitTeachers')
    sheet2 = gc.open('StreamlitStudents')
except gspread.exceptions.SpreadsheetNotFound:
    # If the sheet doesn't exist, create a new one
    sheet2 = gc.create('StreamlitStudents')

# Get the first worksheet
worksheet = sheet.get_worksheet(0)
worksheet2 = sheet2.get_worksheet(0)

data = worksheet.get_all_records()
df = pd.DataFrame(data)

try:
    values = worksheet2.get_all_values()
    if values:
        df2 = pd.DataFrame(values[1:], columns=values[0])
    else:
        df2 = pd.DataFrame(columns=['Erp','Question', 'Markscheme 1', 'Markscheme 2'])
except gspread.exceptions.APIError:
    df2 = pd.DataFrame(columns=['Erp','Question','Markscheme 1','Markscheme 2,Response'])

df.to_csv('data2.csv', index=False)
df2.to_csv('data3.csv', index=False)
questions = df['Question'].tolist()
markingscheme1 = df['Markscheme 1'].tolist()
markingscheme2 = df['Markscheme 2'].tolist()

student_name = st.text_input('Enter your ERP:')

if student_name:
    for i, question in enumerate(questions):
        st.write(f"Question {i + 1}: {question}")
        answer = st.text_area(f'Enter your answer to Question {i + 1} here:', key=f'Response_{i}')

        if st.button(f'Submit Answer to Question {i + 1}'):
            new_row = {'Erp': student_name, 'Question': question, 'Markscheme 1': markingscheme1[i], 'Markscheme 2': markingscheme2[i], 'Response': answer}
            new_row_df = pd.DataFrame([new_row])
            df2 = pd.concat([df2, new_row_df], axis=0)
            worksheet2.update([df2.columns.values.tolist()] + df2.values.tolist(), value_input_option='RAW')
            df.to_csv('data3.csv', index=False)
            df2.to_csv('data4.csv', index=False)
