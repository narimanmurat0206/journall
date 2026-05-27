import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Журнал учета времени", layout="centered")
st.title("🕒 Журнал учета рабочего времени")

EMPLOYEES = ["Сотрудник 1", "Сотрудник 2", "Сотрудник 3", "Сотрудник 4", "Сотрудник 5"]
DB_FILE = "attendance_log.csv"

if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Сотрудник", "Дата", "Статус", "Время"])

st.write("### Отметить сотрудника:")
selected_emp = st.selectbox("Выберите сотрудника:", EMPLOYEES)

col1, col2 = st.columns(2)
with col1:
    if st.button("🟢 ПРИШЕЛ", use_container_width=True):
        now = datetime.now()
        new_row = {"Сотрудник": selected_emp, "Дата": now.strftime("%d.%m.%Y"), "Статус": "Приход", "Время": now.strftime("%H:%M:%S")}
        df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.success(f"✅ {selected_emp} отмечен: Приход в {new_row['Время']}")

with col2:
    if st.button("🔴 УШЕЛ", use_container_width=True):
        now = datetime.now()
        new_row = {"Сотрудник": selected_emp, "Дата": now.strftime("%d.%m.%Y"), "Статус": "Уход", "Время": now.strftime("%H:%M:%S")}
        df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
        df.to_csv(DB_FILE, index=False)
        st.error(f"❌ {selected_emp} отмечен: Уход в {new_row['Время']}")

st.write("---")
st.write("### 📋 Длинный журнал посещаемости:")
if not df.empty:
    st.dataframe(df, use_container_width=True, height=400)
else:
    st.info("Журнал пока пуст.")
