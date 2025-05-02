import tkinter as tk
from tkinter import ttk

class InitialScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Bem-vindo ao DashMovies", font=("Arial", 24)).pack(pady=20)
        ttk.Button(self, text="Busca de Filmes", command=lambda: controller.show_frame("MovieSearchScreen")).pack(pady=10)
        ttk.Button(self, text="Quiz",          command=lambda: controller.show_frame("QuizStartScreen")).pack(pady=10)
        ttk.Button(self, text="Configurações", command=lambda: controller.show_frame("QuizSettingsScreen")).pack(pady=10)
        ttk.Button(self, text="Sair",          command=controller.destroy).pack(pady=10)