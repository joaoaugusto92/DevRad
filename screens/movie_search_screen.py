import tkinter as tk
from tkinter import ttk
import pandas as pd
from ttkbootstrap import Entry
from services.moviesService import search_movies, get_distinct_genres

GENRES = get_distinct_genres()

class MovieSearchScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Carrega base de dados de filmes
        self.df = pd.read_csv(
            "DataSet/world_imdb_movies_top_movies_per_year.csv",
            sep=",", encoding="utf-8"
        )
        self.genre_var = tk.StringVar()
        self._build_search_ui()

    def _clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def _build_search_ui(self):
        """Exibe a interface de busca de filmes."""
        self._clear_frame()
        ttk.Label(
            self,
            text="Saiba mais sobre seu filme favorito",
            font=("Arial", 20)
        ).pack(pady=10)

        # Campo de entrada de pesquisa com bootstyle light para fundo branco
        self.entry = Entry(self, bootstyle="light", width=50)
        self.entry.insert(0, "Digite o título do filme (em inglês)")
        self.entry.pack(pady=5)
        self.entry.bind("<FocusIn>", self._clear_placeholder)


        # Container for Comboboxes
        combobox_frame = ttk.Frame(self)
        combobox_frame.pack(pady=(20, 5))

        # Seleção de Gêneros
        ttk.Label(combobox_frame, text="Gêneros").grid(row=0, column=0, padx=5)
        genre_combobox = ttk.Combobox(combobox_frame, values=[""] + GENRES, textvariable=self.genre_var, state="readonly")
        genre_combobox.grid(row=1, column=0, padx=5)
        

        # Seleção de Décadas
        ttk.Label(combobox_frame, text="Décadas").grid(row=0, column=1, padx=5)
        self.decade_var = tk.StringVar()
        decades = [str(year) for year in range(1960, 2024, 10)]  # Gera décadas de 1900 a 2020
        decade_combobox = ttk.Combobox(combobox_frame, values=[""] + decades, textvariable=self.decade_var, state="readonly")
        decade_combobox.grid(row=1, column=1, padx=5)
        

        # Botões de ação
        ttk.Button(
            self,
            text="Pesquisar Filme",
            command=self._perform_search
        ).pack(pady=5)
        ttk.Button(
            self,
            text="Voltar",
            command=lambda: self.controller.show_frame("InitialScreen")
        ).pack(pady=10)

    def _clear_placeholder(self, event):
        """Limpa o texto de placeholder ao focar no campo."""
        if self.entry.get() == "Digite o título do filme (em inglês)":
            self.entry.delete(0, tk.END)

    def _perform_search(self):
        pesquisa = self.entry.get().strip()
        resultados = search_movies(
            keyword=pesquisa if pesquisa.lower() != "digite o título do filme (em inglês)" else None,
            genre=self.genre_var.get(),
            decade=self.decade_var.get()
        )

        # Formata gross_world_wide para o formato arredondado com K, M, B
        def format_amount(amount):
            if pd.isnull(amount):
                return "N/A"
            elif amount >= 1_000_000_000:
                return f"{amount / 1_000_000_000:.1f}B"
            elif amount >= 1_000_000:
                return f"{amount / 1_000_000:.1f}M"
            elif amount >= 1_000:
                return f"{amount / 1_000:.1f}K"
            else:
                return f"{amount:.0f}"
        resultados["gross_world_wide"] = resultados["gross_world_wide"].apply(format_amount)
        # Limpa os filtros selecionados
        self.genre_var.set("")
        self.decade_var.set("")
        # Exibe os resultados
        self._show_results(resultados, pesquisa)

    def _show_results(self, resultados, pesquisa):
        """Exibe os resultados em um canvas rolável com paginação."""
        self._clear_frame()

        # Configuração de paginação
        self.results_per_page = 50
        self.current_page = 0
        self.resultados = resultados

        def display_page(page):
            """Exibe os resultados da página especificada."""
            self.current_page = page
            for widget in scrollable_frame.winfo_children():
                widget.destroy()

            start_idx = page * self.results_per_page
            end_idx = start_idx + self.results_per_page
            page_results = self.resultados.iloc[start_idx:end_idx]

            if not page_results.empty:
                for _, filme in page_results.iterrows():
                    filme_str = (
                        f"Título: {filme['title']}\n"
                        f"Ano: {filme['year']}\n"
                        f"Gênero: {filme['genre']}\n"
                        f"Duração: {filme['duration']}\n"
                        f"Oscar: {filme['oscar']}\n"
                        f"Nota IMDB: {filme['rating_imdb']}\n"
                        f"Bilheteria mundial: {filme['gross_world_wide']}\n"
                    )
                    ttk.Label(
                        scrollable_frame,
                        text=filme_str,
                        justify="left",
                        anchor="w",
                        font=("Arial", 10)
                    ).pack(fill="x", padx=20, pady=5)
                    ttk.Separator(
                        scrollable_frame,
                        orient="horizontal"
                    ).pack(fill="x", padx=20, pady=2)
            else:
                ttk.Label(
                    scrollable_frame,
                    text=f"Nenhum filme encontrado com: '{pesquisa}'",
                    foreground="red",
                    font=("Arial", 12)
                ).pack(pady=20)

            # Atualiza os botões de navegação
            prev_btn["state"] = "normal" if page > 0 else "disabled"
            next_btn["state"] = "normal" if end_idx < len(self.resultados) else "disabled"

        # Botões para nova busca ou menu
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill="x", pady=5)
        ttk.Button(
            btn_frame,
            text="Nova Busca",
            command=self._build_search_ui
        ).pack(side="left", padx=10)
        ttk.Button(
            btn_frame,
            text="Voltar ao Menu",
            command=lambda: self.controller.show_frame("InitialScreen")
        ).pack(side="left")

        # Canvas e scrollbar
        canvas = tk.Canvas(self)
        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=canvas.yview
        )
        scrollable_frame = ttk.Frame(canvas)
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Habilita rolagem com roda do mouse
        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(int(-1 * (e.delta / 120)), "units")
        )

        # Botões de navegação para paginação
        nav_frame = ttk.Frame(self)
        nav_frame.pack(fill="x", pady=10)

        prev_btn = ttk.Button(
            nav_frame,
            text="Anterior",
            command=lambda: display_page(self.current_page - 1)
        )
        prev_btn.pack(side="left", padx=10)

        next_btn = ttk.Button(
            nav_frame,
            text="Próximo",
            command=lambda: display_page(self.current_page + 1)
        )
        next_btn.pack(side="right", padx=10)

        # Exibe a primeira página
        display_page(0)
