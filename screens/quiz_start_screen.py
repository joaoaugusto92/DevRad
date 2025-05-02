import tkinter as tk
from tkinter import ttk

class QuizStartScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="DashMovies", font=("Arial", 36)).pack(pady=40)
        ttk.Button(
            self,
            text="Iniciar Quiz",
            command=self._go_to_quiz
        ).pack(pady=10)
        ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("InitialScreen")).pack(pady=10)

    def _go_to_quiz(self):
        quiz_screen = self.controller.frames["QuizScreen"]
        quiz_screen.start_quiz()  # inicializa o quiz (perguntas, timer, etc)
        self.controller.show_frame("QuizScreen")  # exibe a tela do quiz