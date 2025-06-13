import sqlite3
import pandas as pd
import os

EXCEL_FILE = "Top3000EngWorld.xlsx"
DB_FILE = "words.db"

def create_table():
    """Создаёт таблицу words в базе данных, если она не существует."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS words (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        word TEXT NOT NULL,
        part_of_speech TEXT,
        transcription TEXT,
        translation TEXT NOT NULL,
        audio_file TEXT
    )
    """)

    conn.commit()
    conn.close()

def import_from_excel():
    """Импортирует данные из Excel в таблицу words."""
    if not os.path.exists(EXCEL_FILE):
        print(f"❌ Файл {EXCEL_FILE} не найден!")
        return

    # Загружаем Excel-файл
    df = pd.read_excel(EXCEL_FILE)

    # Переименование нужных колонок
    df = df.rename(columns={
        "Word": "word",
        "Part of Speech": "part_of_speech",
        "Transcription": "transcription",
        "Translation": "translation"
    })

    required_columns = {"word", "part_of_speech", "transcription", "translation"}
    if not required_columns.issubset(df.columns):
        print("❌ После переименования отсутствуют нужные столбцы!")
        print(f"Текущие столбцы: {set(df.columns)}")
        return

    # Подключение к БД и загрузка данных
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    for _, row in df.iterrows():
        cursor.execute("""
        INSERT INTO words (word, part_of_speech, transcription, translation, audio_file)
        VALUES (?, ?, ?, ?, NULL)
        """, (
            row['word'],
            row['part_of_speech'],
            row['transcription'],
            row['translation']
        ))

    conn.commit()
    conn.close()
    print("✅ Данные успешно импортированы в базу данных!")

# Тестовый запуск
if __name__ == "__main__":
    create_table()
    import_from_excel()
