import sqlite3
import os
import random

# Имя файла базы данных
DB_FILE = "words.db"

def connect_to_db():
    """Подключение к базе данных SQLite."""
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError("❌ База данных words.db не найдена.")
    return sqlite3.connect(DB_FILE)

def get_all_words():
    """Возвращает все слова из таблицы words."""
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT word, part_of_speech, transcription, translation FROM words")
    words = cursor.fetchall()
    conn.close()
    return words

def get_random_words(count=5):
    """Возвращает случайный список слов из таблицы."""
    words = get_all_words()
    if count > len(words):
        count = len(words)
    return random.sample(words, count)

# 🧪 Тестирование — можно закомментировать после проверки
if __name__ == "__main__":
    print("🔍 Тест подключения к базе и выборки слов...")
    try:
        words = get_random_words(5)
        for w in words:
            print(f"📘 {w[0]} [{w[2]}] — {w[3]}")
    except Exception as e:
        print(f"❌ Ошибка: {e}")
