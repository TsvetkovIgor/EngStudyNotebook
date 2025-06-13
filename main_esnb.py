import time
from sqlite_esnb import get_all_words
import random

def study_words(word_list):
    """
    Этап запоминания слов: показывает слова по порядку.
    """
    print("\n📚 Этап 1. Запоминание слов:")
    for i, word_data in enumerate(word_list, 1):
        word, part, transcr, translation = word_data
        print(f"\n{i}. {word} [{transcr}] — {translation}")
        input("Нажмите Enter для следующего слова...")

    print("\n✅ Все слова показаны. Готовы перейти к тесту?")


def run_test(word_list):
    """
    Этап тестирования запомненных слов.
    """
    print("\n🧪 Этап 2. Тест на запоминание:")
    random.shuffle(word_list)

    remaining = word_list.copy()
    score = 0
    incorrect = []

    while remaining:
        current = remaining.pop(0)
        word, part, transcr, translation = current

        print(f"\nСлово: {word}")
        answer = input("Введите перевод: ").strip().lower()

        if answer == translation.strip().lower():
            print("✅ Верно!")
            score += 1
        else:
            print(f"❌ Неверно. Правильный ответ: {translation}")
            incorrect.append(current)

    # Повторить ошибочные
    if incorrect:
        print("\n🔁 Повторим слова, в которых были ошибки...")
        run_test(incorrect)
    else:
        print("\n🎉 Вы правильно ответили на все слова!")

    print(f"\n🎯 Итого правильно: {score} из {len(word_list)}")


if __name__ == "__main__":
    print("Добро пожаловать в EngStudyNotebook (консольная версия)")
    print("📌 Сегодня вы изучите 5 новых слов")

    # Получаем 5 первых слов по порядку (а не случайно)
    full_list = get_all_words()
    new_words = full_list[:5]

    study_words(new_words)

    choice = input("Начать тест? (y/n): ").strip().lower()
    if choice == 'y':
        run_test(new_words)
    else:
        print("Выход без тестирования.")

