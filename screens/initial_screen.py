import tkinter as tk
from tkinter import ttk

class InitialScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Frame central para alinhar tudo no meio
        central_frame = ttk.Frame(self)
        central_frame.pack(expand=True)

        ttk.Label(
            central_frame,
            text="Bem-vindo ao DashMovies",
            font=("Arial", 28, "bold")
        ).pack(pady=(30, 30))

        button_style = {"width": 24, "style": "primary.TButton", "padding": 8}

        ttk.Button(
            central_frame,
            text="Busca de Filmes",
            command=lambda: controller.show_frame("MovieSearchScreen"),
            **button_style
        ).pack(pady=8)

        ttk.Button(
            central_frame,
            text="Quiz",
            command=lambda: controller.show_frame("QuizStartScreen"),
            **button_style
        ).pack(pady=8)

        ttk.Button(
            central_frame,
            text="Configurações",
            command=lambda: controller.show_frame("QuizSettingsScreen"),
            **button_style
        ).pack(pady=8)

        ttk.Button(
            central_frame,
            text="Ranking",
            command=lambda: controller.show_frame("RankingScreen"),
            **button_style
        ).pack(pady=8)

        ttk.Button(
            central_frame,
            text="Sair",
            command=controller.destroy,
            width=24,
            style="danger.TButton",
            padding=8
        ).pack(pady=(24, 8))