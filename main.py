import tkinter as tk
from tkinter import filedialog
import pandas as pd
import random


class TestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Тестирование")
        self.load_button = tk.Button(root, text="Загрузить тест", command=self.load_test)
        self.load_button.pack()
        self.questions = None
        self.current_question_index = 0

    def load_test(self):
        filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if filepath:
            self.questions = pd.read_excel(filepath)
            self.randomize_questions_and_answers()  # Вызов метода для рандомизации
            self.display_current_question()

    def display_current_question(self):
        if self.questions is not None and not self.questions.empty:
            question_row = self.questions.iloc[self.current_question_index]
            question_text = question_row['Вопросы']
            answers = question_row['Перемешанные ответы']

            # Очистить окно перед отображением нового вопроса
            for widget in self.root.winfo_children():
                widget.destroy()

            # Отображаем вопрос
            question_label = tk.Label(self.root, text=question_text)
            question_label.pack()

            # Создаем переменную для хранения ответа пользователя
            self.selected_answer = tk.StringVar()

            # Отображаем варианты ответов
            for answer in answers:
                answer_radio = tk.Radiobutton(self.root, text=answer, variable=self.selected_answer, value=answer)
                answer_radio.pack()

            # Кнопка для подтверждения ответа и перехода к следующему вопросу
            confirm_button = tk.Button(self.root, text="Далее", command=self.next_question)
            confirm_button.pack()

    def next_question(self):
        # Проверяем ответ и обновляем счет, если это необходимо
        correct_answer = self.questions.iloc[self.current_question_index]['Правильный ответ']
        if self.selected_answer.get() == correct_answer:
            # Увеличиваем счет
            pass

        # Переходим к следующему вопросу, если это возможно
        if self.current_question_index < len(self.questions) - 1:
            self.current_question_index += 1
            self.display_current_question()
        else:
            # Если вопросы закончились, показываем результат
            pass

    def randomize_questions_and_answers(self):
        # Перемешиваем вопросы
        self.questions = self.questions.sample(frac=1).reset_index(drop=True)

        # Создаем новый столбец для перемешанных ответов
        self.questions['Перемешанные ответы'] = None

        # Перемешиваем ответы для каждого вопроса
        for i in self.questions.index:
            # Здесь 'Ответы' это имя столбца с правильными ответами, убедитесь, что оно совпадает с вашими данными
            correct_answer = self.questions.at[i, 'Правильный ответ']
            # Получаем все остальные ответы и убираем пустые значения (NaN)
            other_answers = [self.questions.at[i, col] for col in self.questions.columns[2:] if
                             not pd.isna(self.questions.at[i, col])]
            # Объединяем правильный ответ с остальными и перемешиваем
            answers = [correct_answer] + other_answers
            random.shuffle(answers)
            # Присваиваем перемешанные ответы в новый столбец
            self.questions.at[i, 'Перемешанные ответы'] = answers

        # Проверка рандомизации (можно убрать после тестирования)
        print(self.questions[['Вопросы', 'Перемешанные ответы']])


# Инициализация приложения
root = tk.Tk()
app = TestApp(root)
root.mainloop()
