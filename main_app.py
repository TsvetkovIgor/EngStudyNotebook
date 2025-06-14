from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from sqlite_esnb import get_all_words
import random


class MainScreen(Screen):
    log_text = StringProperty("Нажмите СТАРТ для начала")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.difficult_words = []   # слова с ошибками
        self.correct_count = 0      # число верных ответов
        self.incorrect_count = 0    # число ошибок
        self.all_words = []
        self.learned_count = 5
        self.learned = []
        self.remaining = []
        self.current = None
        self.direction = 1
        self.state = 'study'

    def on_start(self):
        self.all_words = get_all_words()
        self.learned_count = 5
        self.learned = self.all_words[:self.learned_count]
        self.state = 'study'
        self.show_study()

    def show_study(self):
        self.log_text = ""
        for i, (w, _, tr, t) in enumerate(self.learned, 1):
            self.log_text += f"{i}. {w} [{tr}] — {t}\n"
        self.log_text += "\nНажмите ВВОД, когда готовы к тесту"

    def on_enter(self):
        text = self.ids.user_input.text.strip()
        self.ids.user_input.text = ''
        if self.state == 'study':
            self.log_text += "\nТест начинается!"
            self.state = 'test'
            self.remaining = self.learned.copy()
            random.shuffle(self.remaining)
            self.next_test()
        elif self.state == 'test':
            self.process_answer(text)

    def next_test(self):
        if not self.remaining:
            self.log_text += f"\n🎉 Тест пройден! ✅ {self.correct_count} ❌ {self.incorrect_count}"
            self.correct_count = 0
            self.incorrect_count = 0
            self.learned_count += 1
            if self.learned_count > len(self.all_words):
                self.log_text += "\n🎓 Все слова изучены!"
                return
            self.learned = self.all_words[:self.learned_count]
            self.state = 'study'
            self.show_study()
            return

        self.current = self.remaining.pop()
        self.direction = random.choice([1, 2])
        w, _, tr, t = self.current

        if self.direction == 1:
            self.log_text += f"\n\nСлово: {w}"
        else:
            self.log_text += f"\n\nПеревод: {t}"

    def process_answer(self, text):
        w, _, tr, t = self.current
        answer = text.lower().strip()
        if self.direction == 1:
            correct = t.lower().strip().rstrip(';, .')
            if answer == correct:
                self.log_text += "\n✅ Верно!"
                self.correct_count += 1
            else:
                self.log_text += f"\n❌ Неверно! {t}"
                self.incorrect_count += 1
                self.difficult_words.append(self.current)
                self.remaining.append(self.current)
        else:
            if answer == w.lower():
                self.log_text += "\n✅ Верно!"
                self.correct_count += 1
            else:
                self.log_text += f"\n❌ Неверно! {w}"
                self.incorrect_count += 1
                self.difficult_words.append(self.current)
                self.remaining.append(self.current)

        self.next_test()

    def repeat_difficult(self):
        if not self.difficult_words:
            self.log_text += "\nНет трудных слов для повторения!"
            return
        self.log_text += "\n🔁 Повтор трудных слов:"
        self.remaining = self.difficult_words.copy()
        self.difficult_words.clear()
        random.shuffle(self.remaining)
        self.state = 'test'
        self.correct_count = 0
        self.incorrect_count = 0
        self.next_test()

    def on_exit(self):
        App.get_running_app().stop()


class EngApp(App):
    def build(self):
        from kivy.lang import Builder
        Builder.load_file('ui.kv')
        return MainScreen()


if __name__ == '__main__':
    EngApp().run()
