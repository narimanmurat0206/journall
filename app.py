import streamlit as str
import pandas as pd
import datetime
import os

# Настройка названия страницы
str.set_page_config(page_title="Журнал учета заказов", layout="wide")
str.title("📋 Общий журнал учета работы")

# Файл для хранения общей базы данных
DB_FILE = "journal_data.csv"

# Загрузка существующих данных
if os.path.exists(DB_FILE):
    df = pd.read_csv(DB_FILE)
else:
    df = pd.DataFrame(columns=["Учетное время", "Сотрудник / Заказ", "Этап работы"])

# --- ФОРМА ВВОДА ---
str.subheader("➕ Добавить новую отметку")

with str.form("journal_form", clear_on_submit=True):
    col1, col2 = str.columns(2)
    
    with col1:
        name = str.text_input("Введите имя сотрудника или номер заказа:")
    
    with col2:
        status = str.selectbox(
            "Выберите этап работы:",
            [
                "📥 Жумыс келди (Работа поступила)",
                "⚙️ Жумыс стелип жатыр (В процессе)",
                "🪡 Примерка",
                "✅ Сдача"
            ]
        )
    
    submit = str.form_submit_button("Сохранить в общий журнал")

# Если кнопка нажата, записываем данные
if submit and name:
    # Берем текущее время (Казахстан / локальное)
    current_time = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    
    # Новая строчка
    new_row = pd.DataFrame([[current_time, name, status]], columns=["Учетное время", "Сотрудник / Заказ", "Этап работы"])
    
    # Добавляем в общую таблицу
    df = pd.concat([new_row, df], ignore_index=True)
    df.to_csv(DB_FILE, index=False)
    str.success("Данные успешно добавлены!")
    str.rerun()

# --- ВЫВОД ОБЩЕЙ ТАБЛИЦЫ ---
str.markdown("---")
str.subheader("📖 Общая тетрадь (Все записи)")

if not df.empty:
    str.dataframe(df, use_container_width=True)
else:
    str.info("Журнал пока пуст. Добавьте первую запись выше.")
