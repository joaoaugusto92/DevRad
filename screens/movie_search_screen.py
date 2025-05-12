import tkinter as tk
from tkinter import ttk
import pandas as pd
from ttkbootstrap import Entry

GENRES = ['Erotic Thriller'
, 'Giallo'
, 'Slasher Horror'
, 'Horror'
, 'Mystery'
, 'Thriller'
, 'Parody'
, 'Slapstick'
, 'Comedy'
, 'Drama'
, 'Romance'
, 'Satire'
, 'Sketch Comedy'
, 'Action'
, 'Adventure'
, 'Crime'
, 'Family'
, 'Biography'
, 'Martial Arts'
, 'Fantasy'
, 'Psychological Drama'
, 'HandDrawn Animation'
, 'Quest'
, 'Animation'
, 'War'
, 'Music'
, 'Documentary'
, 'Police Procedural'
, 'Western'
, 'Classical Western'
, 'Musical'
, 'Romantic Comedy'
, 'Fairy Tale'
, 'Stop Motion Animation'
, 'History'
, 'SciFi'
, 'History Documentary'
, 'Globetrotting Adventure'
, 'Superhero'
, 'Psychological Thriller'
, 'Suspense Mystery'
, 'Zombie Horror'
, 'Anime'
, 'Holiday Romance'
, 'Holiday'
, 'nan'
, 'Dark Fantasy'
, 'Vampire Horror'
, 'Disaster'
, 'Tragedy'
, 'Dark Comedy'
, 'Adult Animation'
, 'Mecha'
, 'Action Epic'
, 'Adventure Epic'
, 'Fantasy Epic'
, 'SciFi Epic'
, 'Space SciFi'
, 'Drug Crime'
, 'Buddy Comedy'
, 'Computer Animation'
, 'Farce'
, 'HighConcept Comedy'
, 'Urban Adventure'
, 'Teen Horror'
, 'Conspiracy Thriller'
, 'Cyber Thriller'
, 'Found Footage Horror'
, 'Science  Technology Documentary'
, 'Sea Adventure'
, 'Swashbuckler'
, 'Workplace Drama'
, 'ComingofAge'
, 'Teen Drama'
, 'Nature Documentary'
, 'Football'
, 'Sports Documentary'
, 'Sport'
, 'Tragic Romance'
, 'Folk Horror'
, 'Car Action'
, 'Road Trip'
, 'Sword  Sorcery'
, 'Pop Musical'
, 'BHorror'
, 'Prison Drama'
, 'Spy'
, 'Kung Fu'
, 'OnePerson Army Action'
, 'Wuxia'
, 'Political Thriller'
, 'Caper'
, 'Supernatural Horror'
, 'Witch Horror'
, 'Contemporary Western'
, 'Steamy Romance'
, 'Psychological Horror'
, 'Cop Drama'
, 'FeelGood Romance'
, 'StandUp'
, 'Baseball'
, 'Medical Drama'
, 'Buddy Cop'
, 'Heist'
, 'Period Drama'
, 'Animal Adventure'
, 'Raunchy Comedy'
, 'War Epic'
, 'Docudrama'
, 'Basketball'
, 'True Crime'
, 'Screwball Comedy'
, 'Samurai'
, 'Quirky Comedy'
, 'Dark Romance'
, 'Monster Horror'
, 'Jungle Adventure'
, 'Body Swap Comedy'
, 'Showbiz Drama'
, 'Supernatural Fantasy'
, 'Teen Comedy'
, 'Artificial Intelligence'
, 'Dystopian SciFi'
, 'News'
, 'Teen Romance'
, 'Legal Drama'
, 'Legal Thriller'
, 'Teen Adventure'
, 'Music Documentary'
, 'Body Horror'
, 'Alien Invasion'
, 'Survival'
, 'Whodunnit'
, 'Boxing'
, 'Political Drama'
, 'Costume Drama'
, 'Concert'
, 'Financial Drama'
, 'Extreme Sport'
, 'Dinosaur Adventure'
, 'Time Travel'
, 'Food Documentary'
, 'Epic'
, 'Romantic Epic'
, 'Kaiju'
, 'Spaghetti Western'
, 'Werewolf Horror'
, 'Desert Adventure'
, 'Gangster'
, 'Mockumentary'
, 'Steampunk'
, 'Sword  Sandal'
, 'Bumbling Detective'
, 'Holiday Animation'
, 'Holiday Comedy'
, 'Holiday Family'
, 'Jukebox Musical'
, 'BAction'
, 'Cyberpunk'
, 'Military Documentary'
, 'Teen Fantasy'
, 'Historical Epic'
, 'Soccer'
, 'Mountain Adventure'
, 'Shjo'
, 'Seinen'
, 'Shnen'
, 'Faith  Spirituality Documentary'
, 'Travel Documentary'
, 'Serial Killer'
, 'Gun Fu'
, 'Stoner Comedy'
, 'Western Epic'
, 'Water Sport'
, 'Motorsport'
, 'Isekai'
, 'Crime Documentary'
, 'Cozy Mystery'
, 'Hardboiled Detective'
, 'Iyashikei'
, 'Political Documentary'
, 'Rock Musical'
, 'Sitcom'
, 'Splatter Horror'
, 'Classic Musical'
, 'Korean Drama'
, 'Slice of Life'
, 'Talk Show'
, 'Reality TV'
, 'Game Show'
, 'Josei'
, 'Soap Opera']

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





    def search_movies_filters(self):
        try:
            movies_df = pd.read_csv("DataSet/world_imdb_movies_top_movies_per_year.csv")
            filtered_movies = movies_df.copy()
            
            # Aplica filtro de gênero se selecionado
            selected_genre = self.genre_var.get()
            if selected_genre and selected_genre != "":
                filtered_movies = filtered_movies[filtered_movies['genre'].str.contains(selected_genre, na=False, case=False)]
            
            # Aplica filtro de década se selecionado
            selected_decade = self.decade_var.get()
            if selected_decade and selected_decade != "":
                start_year = int(selected_decade)
                end_year = start_year + 9
                filtered_movies['year'] = pd.to_numeric(filtered_movies['year'], errors='coerce')
                filtered_movies = filtered_movies[(filtered_movies['year'] >= start_year) & 
                                                (filtered_movies['year'] <= end_year)]
            
            if not filtered_movies.empty:
                print(f"Filmes encontrados com os filtros aplicados:")
                print(filtered_movies[['title', 'genre', 'year']])
                return filtered_movies
            else:
                print("Nenhum filme encontrado com os filtros aplicados.")
                return None
                
        except Exception as e:
            print(f"Ocorreu um erro ao buscar filmes: {e}")
            return None







    def _clear_placeholder(self, event):
        """Limpa o texto de placeholder ao focar no campo."""
        if self.entry.get() == "Digite o título do filme (em inglês)":
            self.entry.delete(0, tk.END)

    def _perform_search(self):
        """Realiza a busca com base no título, gênero e década."""
        pesquisa = self.entry.get().strip().lower()
        resultados = self.df.copy()

        # Filtro por nome (se houver)
        if pesquisa and pesquisa != "digite o título do filme (em inglês)":
            resultados = resultados[
                resultados["title"].str.lower().apply(
                    lambda x: all(word in x for word in pesquisa.split())
                )
            ]

        # Filtro por gênero
        selected_genre = self.genre_var.get()
        if selected_genre:
            resultados = resultados[resultados['genre'].str.contains(selected_genre, na=False, case=False)]

        # Filtro por década
        selected_decade = self.decade_var.get()
        if selected_decade:
            start_year = int(selected_decade)
            end_year = start_year + 9
            resultados['year'] = pd.to_numeric(resultados['year'], errors='coerce')
            resultados = resultados[(resultados['year'] >= start_year) & (resultados['year'] <= end_year)]

        # Ordena por bilheteria
        resultados = resultados.sort_values(by="gross_world_wide", ascending=False)

        
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
        self._show_results(resultados, pesquisa)

    def _show_results(self, resultados, pesquisa):
        """Exibe os resultados em um canvas rolável."""
        self._clear_frame()
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

        # Exibe resultados formatados
        if not resultados.empty:
            for _, filme in resultados.iterrows():
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
