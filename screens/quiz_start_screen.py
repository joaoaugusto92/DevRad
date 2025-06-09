import tkinter as tk
from tkinter import ttk
from services.moviesService import get_distinct_genres
from data.questions import get_questions

GENRES = get_distinct_genres()

class QuizStartScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        ttk.Label(self, text="DashMovies", font=("Arial", 36)).pack(pady=40)
        self.genre_var = tk.StringVar()
        self.decade_var = tk.StringVar()

        # Filtros de gênero e década (sempre visíveis)
        combobox_frame = ttk.Frame(self)
        combobox_frame.pack(pady=(20, 5))

        ttk.Label(combobox_frame, text="Gêneros").grid(row=0, column=0, padx=5)
        genre_combobox = ttk.Combobox(combobox_frame, values=GENRES, textvariable=self.genre_var, state="readonly")
        genre_combobox.grid(row=1, column=0, padx=5)

        ttk.Label(combobox_frame, text="Décadas").grid(row=0, column=1, padx=5)
        decades = [str(year) for year in range(1960, 2024, 10)]
        decade_combobox = ttk.Combobox(combobox_frame, values=decades, textvariable=self.decade_var, state="readonly")
        decade_combobox.grid(row=1, column=1, padx=5)

        # Botões de ação (sempre visíveis)
        ttk.Button(
            self,
            text="Iniciar Quiz",
            style="success.TButton",
            command=self._go_to_quiz
        ).pack(pady=10)

        ttk.Button(
            self,
            text="Voltar",
            style="secondary.TButton",
            command=lambda: controller.show_frame("InitialScreen")
        ).pack(pady=10)

    def _go_to_quiz(self):
        QUESTIONS = get_questions(
            genre=self.genre_var.get() or None,
            decade=self.decade_var.get() or None,
            top_n=15
        )
        quiz_screen = self.controller.frames["QuizScreen"]
        quiz_screen.start_quiz(QUESTIONS)
        self.controller.show_frame("QuizScreen")