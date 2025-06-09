import tkinter as tk
from tkinter import ttk

class InitialScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Frame central para alinhar tudo no meio
        self.central_frame = ttk.Frame(self)
        self.central_frame.pack(expand=True)

        self.username_label = ttk.Label(self.central_frame, font=("Arial", 14))
        self.username_label.pack(pady=(10, 0))

        ttk.Label(
            self.central_frame,
            text="Bem-vindo ao DashMovies",
            font=("Arial", 28, "bold")
        ).pack(pady=(10, 30))

        button_style = {"width": 24, "style": "primary.TButton", "padding": 8}

        ttk.Button(
            self.central_frame,
            text="Busca de Filmes",
            command=lambda: controller.show_frame("MovieSearchScreen"),
            **button_style
        ).pack(pady=8)

        ttk.Button(
            self.central_frame,
            text="Quiz",
            command=lambda: controller.show_frame("QuizStartScreen"),
            **button_style
        ).pack(pady=8)

        ttk.Button(
            self.central_frame,
            text="Configurações",
            command=lambda: controller.show_frame("QuizSettingsScreen"),
            **button_style
        ).pack(pady=8)

        ttk.Button(
            self.central_frame,
            text="Ranking",
            command=lambda: controller.show_frame("RankingScreen"),
            **button_style
        ).pack(pady=8)

        # Botão de admin, só aparece para admins
        self.admin_button = ttk.Button(
            self.central_frame,
            text="Gerenciar Usuários",
            command=lambda: controller.show_frame("AdminPlayersScreen"),
            **button_style
        )
        # Não empacota aqui, só no on_show se for admin

        ttk.Button(
            self.central_frame,
            text="Sair",
            command=controller.destroy,
            width=24,
            style="danger.TButton",
            padding=8
        ).pack(pady=(24, 8))

    def on_show(self):
        user = getattr(self.controller, "current_user", None)
        if user:
            self.username_label.config(text=f"Usuário: {user[1]}")
            self.username_label.pack()
            if len(user) > 2 and user[2]:  # is_admin
                # Empacota o botão admin acima do botão Sair
                self.admin_button.pack_forget()
                # Encontra o botão Sair e empacota o admin_button antes dele
                sair_btn = None
                for widget in self.central_frame.winfo_children():
                    if isinstance(widget, ttk.Button) and widget['text'] == 'Sair':
                        sair_btn = widget
                        break
                if sair_btn:
                    self.admin_button.pack(pady=8, before=sair_btn)
                else:
                    self.admin_button.pack(pady=8)
            else:
                self.admin_button.pack_forget()
        else:
            self.username_label.config(text="")
            self.admin_button.pack_forget()