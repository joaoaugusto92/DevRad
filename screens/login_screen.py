from tkinter import ttk, messagebox
import tkinter as tk
from data.players_db import authenticate_player, add_player

class LoginScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Login", font=("Arial", 20, "bold")).pack(pady=20)
        ttk.Label(self, text="Email:").pack()
        self.email_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.email_var).pack()
        ttk.Label(self, text="Senha:").pack()
        self.senha_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.senha_var, show="*").pack()
        ttk.Button(self, text="Entrar", style="primary.TButton", command=self.login).pack(pady=10)
        ttk.Button(self, text="Cadastrar", style="info.TButton", command=self.cadastro_popup).pack()


    def login(self):
        email = self.email_var.get()
        senha = self.senha_var.get()
        user = authenticate_player(email, senha)
        if user:
            self.controller.current_user = user
            if user[2]:  # is_admin == 1
                self.controller.show_frame("AdminPlayersScreen")
            else:
                self.controller.show_frame("QuizStartScreen")
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos.")

    def cadastro_popup(self):
        top = tk.Toplevel(self)
        top.title("Cadastro")
        nome_var = tk.StringVar()
        email_var = tk.StringVar()
        senha_var = tk.StringVar()
        ttk.Label(top, text="Nome:").pack()
        ttk.Entry(top, textvariable=nome_var).pack()
        ttk.Label(top, text="Email:").pack()
        ttk.Entry(top, textvariable=email_var).pack()
        ttk.Label(top, text="Senha:").pack()
        ttk.Entry(top, textvariable=senha_var, show="*").pack()
        def cadastrar():
            add_player(nome_var.get(), email_var.get(), senha_var.get())
            messagebox.showinfo("Sucesso", "Cadastro realizado!")
            # Login automático após cadastro
            user = authenticate_player(email_var.get(), senha_var.get())
            if user:
                self.controller.current_user = user
            top.destroy()
            self.controller.show_frame("QuizStartScreen")
        ttk.Button(top, text="Cadastrar", style="success.TButton", command=cadastrar).pack(pady=10)