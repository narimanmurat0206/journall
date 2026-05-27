import streamlit as str
import pandas as pd
import datetime
import os

str.set_page_config(page_title="Журнал учета заказов", layout="wide")
str.title("📋 Общий журнал учета работы")

DB_FILE = "journal_data.csv"

# Загрузка данных
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
    # Гарантируем, что колонка ID существует
    if "ID" not in df.columns:
        df["ID"] = range(1, len(df) + 1)
else:
    df = pd.DataFrame(columns=["ID", "Учетное время", "Сотрудник / Заказ", "Этап работы"])

# --- ФОРМА ВВОДА (Новый заказ) ---
str.subheader("➕ Добавить новый заказ / сотрудника")
with str.form("journal_form", clear_on_submit=True):
    col1, col2 = str.columns(2)
    with col1:
        name = str.text_input("Введите имя сотрудника или номер заказа:")
    with col2:
        status = str.selectbox(
            "Выберите начальный этап:",
            ["📥 Жумыс келди", "⚙️ Жумыс стелип жатыр", "🪡 Примерка", "✅ Сдача"]
        )
    submit = str.form_submit_button("Добавить в журнал")

if submit and name:
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    next_id = int(df["ID"].max() + 1) if not df.empty else 1
    new_row = pd.DataFrame([[next_id, current_time, name, status]], columns=["ID", "Учетное время", "Сотрудник / Заказ", "Этап работы"])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    str.success("Заказ добавлен!")
    str.rerun()

# --- ФОРМА ИЗМЕНЕНИЯ СТАТУСА ---
if not df.empty:
    str.markdown("---")
    str.subheader("🔄 Изменить этап существующего заказа")
    
    with str.form("update_form"):
        col_select, col_status, col_btn = str.columns([2, 2, 1])
        
        with col_select:
            # Создаем список для выбора: "ID: Имя заказа (Текущий статус)"
            options = df.apply(lambda r: f"{int(r['ID'])}: {r['Сотрудник / Заказ']} ({r['Этап работы']})", axis=1).tolist()
            selected_option = str.selectbox("Выберите заказ для обновления:", options)
        
        with col_status:
            new_status = str.selectbox(
                "Установите НОВЫЙ этап:",
                ["📥 Жумыс келди", "⚙️ Жумыс стелип жатыр", "🪡 Примерка", "✅ Сдача"]
            )
            
        with col_btn:
            str.write("") # Смещение для выравнивания кнопки
            str.write("")
            update_submit = str.form_submit_button("Обновить статус")
            
    if update_submit:
        selected_id = int(selected_option.split(":")[0])
        current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        
        # Обновляем этап и время изменения для выбранного ID
        df.loc[df["ID"] == selected_id, "Этап работы"] = new_status
        df.loc[df["ID"] == selected_id, "Учетное время"] = current_time
        
        df.to_csv(DB_FILE, index=False)
        str.success("Статус успешно обновлен!")
        str.rerun()

# --- ВЫВОД ТАБЛИЦЫ ---
str.markdown("---")
str.subheader("📖 Текущее состояние всех заказов")

if not df.empty:
    # Показываем таблицу без колонки ID, чтобы не путать
    str.dataframe(df[["Учетное время", "Сотрудник / Заказ", "Этап работы"]], use_container_width=True)
else:
    str.info("Журнал пока пуст.")
