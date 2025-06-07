import tkinter as tk
from tkinter import ttk, messagebox
from data.players_db import get_players, add_player, update_player, delete_player

class AdminPlayersScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self._build_ui()
        self._refresh_tree()

    def _build_ui(self):
        self.tree = ttk.Treeview(self, columns=("ID", "Nome", "Email"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Email", text="Email")
        self.tree.pack(fill="both", expand=True)

        btns = ttk.Frame(self)
        btns.pack(pady=10)
        ttk.Button(btns, text="Adicionar", command=self._add_player).pack(side="left", padx=5)
        ttk.Button(btns, text="Editar", command=self._edit_player).pack(side="left", padx=5)
        ttk.Button(btns, text="Deletar", command=self._delete_player).pack(side="left", padx=5)
        ttk.Button(btns, text="Voltar", command=lambda: self.controller.show_frame("InitialScreen")).pack(side="left", padx=5)

    def _refresh_tree(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for player in get_players():
            self.tree.insert("", "end", values=player)

    def _add_player(self):
        self._open_player_form()

    def _edit_player(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selecione", "Selecione um jogador para editar.")
            return
        item = self.tree.item(selected[0])
        self._open_player_form(item["values"][0], item["values"][1], item["values"][2])

    def _delete_player(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Selecione", "Selecione um jogador para deletar.")
            return
        player_id = self.tree.item(selected[0])["values"][0]
        delete_player(player_id)
        self._refresh_tree()

    def _open_player_form(self, player_id=None, nome="", email=""):
        top = tk.Toplevel(self)
        top.title("Jogador")
        nome_var = tk.StringVar(value=nome)
        email_var = tk.StringVar(value=email)
        ttk.Label(top, text="Nome:").pack()
        ttk.Entry(top, textvariable=nome_var).pack()
        ttk.Label(top, text="Email:").pack()
        ttk.Entry(top, textvariable=email_var).pack()
        def save():
            if player_id is None:
                add_player(nome_var.get(), email_var.get())
            else:
                update_player(player_id, nome_var.get(), email_var.get())
            self._refresh_tree()
            top.destroy()
        ttk.Button(top, text="Salvar", command=save).pack(pady=5)