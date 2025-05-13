import tkinter as tk
from tkinter import ttk
import pandas as pd
from services.moviesService import get_distinct_genres
from data.questions import get_questions

GENRES = get_distinct_genres()

class QuizStartScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="DashMovies", font=("Arial", 36)).pack(pady=40)
        self.controller = controller
        self.genre_var = tk.StringVar()

        # Container para Comboboxes
        combobox_frame = ttk.Frame(self)
        combobox_frame.pack(pady=(20, 5))

        # Seleção de Gêneros
        ttk.Label(combobox_frame, text="Gêneros").grid(row=0, column=0, padx=5)
        genre_combobox = ttk.Combobox(combobox_frame, values=GENRES, textvariable=self.genre_var, state="readonly")
        genre_combobox.grid(row=1, column=0, padx=5)
        # genre_combobox.bind("<<ComboboxSelected>>", self.handle_filter_selection)

        # Seleção de Décadas
        ttk.Label(combobox_frame, text="Décadas").grid(row=0, column=1, padx=5)
        self.decade_var = tk.StringVar()
        decades = [str(year) for year in range(1960, 2024, 10)]  # Gera décadas de 1900 a 2020
        decade_combobox = ttk.Combobox(combobox_frame, values=decades, textvariable=self.decade_var, state="readonly")
        decade_combobox.grid(row=1, column=1, padx=5)
        # decade_combobox.bind("<<ComboboxSelected>>", self.handle_filter_selection)

        ttk.Button(
            self,
            text="Iniciar Quiz",
            command=self._go_to_quiz
        ).pack(pady=10)
        
        ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("InitialScreen")).pack(pady=10)

    def _go_to_quiz(self):
        # Primeiro, busca e imprime os 15 melhores filmes filtrados
        QUESTIONS = get_questions(
            genre=self.genre_var.get() or None,
            decade=self.decade_var.get() or None,
            top_n=15
        )
        # Em seguida, inicia o quiz normalmente
        quiz_screen = self.controller.frames["QuizScreen"]
        quiz_screen.start_quiz(QUESTIONS)
        self.controller.show_frame("QuizScreen")