import tkinter as tk
from tkinter import ttk, messagebox
from data.players_db import (
    get_players, add_player, update_player, delete_player,
    search_players_by_id, search_players_by_name
)
from data.players_db import add_player
add_player("Administrador", "admin@email.com", "senha123", is_admin=1)

class AdminPlayersScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.info_label = ttk.Label(self, font=("Arial", 14, "bold"))
        self.info_label.pack(pady=10)
        self._build_ui()
        self._refresh_tree()

    def on_show(self):
        admin_info = getattr(self.controller, "current_user", None)
        if admin_info:
            self.info_label.config(text=f"Admin: {admin_info[1]} (ID: {admin_info[0]})")
        else:
            self.info_label.config(text="Admin não identificado")

    def _build_ui(self):
        # Campo de busca
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=5)
        ttk.Label(search_frame, text="Buscar por ID:").pack(side="left")
        self.search_id_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_id_var, width=8).pack(side="left", padx=2)
        ttk.Label(search_frame, text="ou Nome:").pack(side="left")
        self.search_name_var = tk.StringVar()
        ttk.Entry(search_frame, textvariable=self.search_name_var, width=15).pack(side="left", padx=2)
        ttk.Button(search_frame, text="Buscar", command=self._search_player).pack(side="left", padx=5)
        ttk.Button(search_frame, text="Limpar", command=self._refresh_tree).pack(side="left", padx=5)

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
        self.search_id_var.set("")
        self.search_name_var.set("")

    def _search_player(self):
        id_val = self.search_id_var.get().strip()
        name_val = self.search_name_var.get().strip()
        results = []
        if id_val:
            try:
                results = search_players_by_id(int(id_val))
            except ValueError:
                messagebox.showwarning("Atenção", "ID deve ser um número inteiro.")
                return
        elif name_val:
            results = search_players_by_name(name_val)
        else:
            messagebox.showinfo("Busca", "Digite um ID ou Nome para buscar.")
            return

        for row in self.tree.get_children():
            self.tree.delete(row)
        for player in results:
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
            if not nome_var.get() or not email_var.get():
                messagebox.showwarning("Campos obrigatórios", "Preencha nome e email.")
                return
            if player_id is None:
                add_player(nome_var.get(), email_var.get(), "senha_padrao")
            else:
                update_player(player_id, nome_var.get(), email_var.get())
            self._refresh_tree()
            top.destroy()

        ttk.Button(top, text="Salvar", command=save).pack(pady=5)
        
   