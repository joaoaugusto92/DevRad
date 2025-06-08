from tkinter import ttk
from data.players_db import get_ranking

class RankingScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Ranking dos Jogadores", font=("Arial", 20, "bold")).pack(pady=20)
        self.tree = ttk.Treeview(self, columns=("Nome", "Pontuação"), show="headings")
        self.tree.heading("Nome", text="Nome")
        self.tree.heading("Pontuação", text="Pontuação")
        self.tree.pack(fill="both", expand=True, padx=20, pady=10)
        ttk.Button(self, text="Voltar", command=lambda: controller.show_frame("InitialScreen")).pack(pady=10)
        self.refresh_ranking()

    def refresh_ranking(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for nome, pontuacao in get_ranking():
            self.tree.insert("", "end", values=(nome, pontuacao))