import time
from sqlite_esnb import get_all_words
import random

def study_words(word_list):
    """Этап показа всех слов с переводами для запоминания"""
    print("\n📚 Этап 1. Запоминание слов:")
    for i, word_data in enumerate(word_list, 1):
        word, part, transcr, translation = word_data
        print(f"\n{i}. {word} [{transcr}] — {translation}")
        input("Нажмите Enter для следующего слова...")

def run_test(word_list):
    """Проводит тест и возвращает True, если все ответы верны"""
    print("\n🧪 Этап 2. Тест на запоминание:")
    random.shuffle(word_list)

    incorrect = []
    for word, part, transcr, translation in word_list:
        print(f"\nСлово: {word}")
        answer = input("Введите перевод: ").strip().lower()

        if answer == translation.strip().lower():
            print("✅ Верно!")
        else:
            print(f"❌ Неверно. Правильный ответ: {translation}")
            incorrect.append((word, part, transcr, translation))

    if incorrect:
        print("\n🔁 Повтор слов с ошибками:")
        return run_test(incorrect)  # рекурсивно повторяем только ошибочные слова
    else:
        print("🎉 Все слова запомнены правильно!")
        return True

def learning_loop():
    """Основной цикл обучения: запомнить → протестировать → расширить список"""
    all_words = get_all_words()
    learned_count = 5
    learned_words = all_words[:learned_count]

    while learned_count <= len(all_words):
        print(f"\n🔄 Текущая группа слов: {learned_count} шт.")
        study_words(learned_words)

        choice = input("Начать тест? (y/n): ").strip().lower()
        if choice != 'y':
            print("🚪 Выход из программы.")
            break

        success = run_test(learned_words)
        if success:
            if learned_count >= len(all_words):
                print("🎓 Все слова изучены! Отличная работа!")
                break

            learned_count += 1  # добавим одно слово
            learned_words = all_words[:learned_count]
            print(f"➕ Добавлено новое слово. Теперь изучаем {learned_count} слов.")
        else:
            print("🔁 Повторение слов, были ошибки...")

if __name__ == "__main__":
    print("👋 Добро пожаловать в EngStudyNotebook!")
    print("Режим: последовательное изучение и тестирование слов.")
    learning_loop()
