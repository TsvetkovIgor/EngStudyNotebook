from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty
from sqlite_esnb import get_all_words, study_words, run_test  # адаптируем после GUI
import random

class MainScreen(Screen):
    log_text = StringProperty("Нажмите СТАРТ для начала")

    def on_start(self):
        self.all_words = get_all_words()
        self.learned_count = 5
        self.learned = self.all_words[:self.learned_count]
        self.state = 'study'  # или 'test'
        self.show_study()

    def show_study(self):
        self.log_text = ""
        for i, (w, _, tr, t) in enumerate(self.learned,1):
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
            self.log_text += "\n🎉 Тест пройден!"
            self.learned_count += 1
            self.learned = self.all_words[:self.learned_count]
            self.state = 'study'
            self.show_study()
            return
        self.current = self.remaining.pop()
        direction = random.choice([1,2])
        self.direction = direction
        w, _, tr, t = self.current
        if direction == 1:
            self.log_text += f"\n\nСлово: {w}"
        else:
            self.log_text += f"\n\nПеревод: {t}"

    def process_answer(self, text):
        w, _, tr, t = self.current
        answer = text.lower()
        if self.direction == 1:
            correct = t.lower().rstrip(';, .')
            if answer == correct:
                self.log_text += "\n✅ Верно!"
            else:
                self.log_text += f"\n❌ Неверно! {t}"
                self.remaining.append(self.current)
        else:
            if answer == w.lower():
                self.log_text += "\n✅ Верно!"
            else:
                self.log_text += f"\n❌ Неверно! {w}"
                self.remaining.append(self.current)
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
