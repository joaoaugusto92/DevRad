import tkinter as tk
from tkinter import ttk
import pandas as pd


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
class QuizStartScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        ttk.Label(self, text="DashMovies", font=("Arial", 36)).pack(pady=40)
        self.controller = controller
        self.genre_var = tk.StringVar()

        # Container for Comboboxes
        combobox_frame = ttk.Frame(self)
        combobox_frame.pack(pady=(20, 5))

        # Seleção de Gêneros
        ttk.Label(combobox_frame, text="Gêneros").grid(row=0, column=0, padx=5)
        genre_combobox = ttk.Combobox(combobox_frame, values=GENRES, textvariable=self.genre_var, state="readonly")
        genre_combobox.grid(row=1, column=0, padx=5)
        genre_combobox.bind("<<ComboboxSelected>>", self.handle_genre_selection)

        # Seleção de Décadas
        ttk.Label(combobox_frame, text="Décadas").grid(row=0, column=1, padx=5)
        self.decade_var = tk.StringVar()
        decades = [str(year) for year in range(1960, 2024, 10)]  # Gera décadas de 1900 a 2020
        decade_combobox = ttk.Combobox(combobox_frame, values=decades, textvariable=self.decade_var, state="readonly")
        decade_combobox.grid(row=1, column=1, padx=5)
        decade_combobox.bind("<<ComboboxSelected>>", self.handle_decade_selection)

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

    def handle_genre_selection(self, event):
        selected_genre = self.genre_var.get()
        print(f"Gênero selecionado: {selected_genre}")
        filtered_movies = self.search_movies_by_genre(selected_genre)
        if filtered_movies is not None:
            # Aqui você pode passar os filmes filtrados para o quiz ou armazená-los
            self.controller.filtered_movies = filtered_movies
        else:
            print("Nenhum filme foi encontrado ou ocorreu um erro.")

    #filtro por gênero
    def search_movies_by_genre(self, genre):
        try:
            # Carregando o dataset 
            movies_df = pd.read_csv("DataSet/world_imdb_movies_top_movies_per_year.csv")
    
            # Filtra os filmes pelo gênero selecionado
            filtered_movies = movies_df[movies_df['genre'].str.contains(genre, na=False, case=False)]
    
            if not filtered_movies.empty:
                print(f"Filmes encontrados para o gênero '{genre}':")
                print(filtered_movies[['title', 'genre']])  # Exibe título e gênero os filmes encontrados  
                return filtered_movies
            else:
                print(f"Nenhum filme encontrado para o gênero '{genre}'.")
        except FileNotFoundError:
                print("Erro: O arquivo do dataset não foi encontrado.")
        except Exception as e:
                print(f"Ocorreu um erro ao buscar filmes: {e}")

    # seleção de Décadas
    def handle_decade_selection(self, event):
        selected_decade = self.decade_var.get()
        print(f"Década selecionada: {selected_decade}")
        filtered_movies = self.search_movies_by_decade(selected_decade)
        if filtered_movies is not None:
            # Aqui você pode passar os filmes filtrados para o quiz ou armazená-los
            self.controller.filtered_movies = filtered_movies
        else:
            print("Nenhum filme foi encontrado ou ocorreu um erro.")

    #filtro por década
    def search_movies_by_decade(self, decade):
        try:
            # Carregando o dataset
            movies_df = pd.read_csv("DataSet/world_imdb_movies_top_movies_per_year.csv")

            # Converte a coluna de ano para inteiro (caso não esteja)
            movies_df['year'] = pd.to_numeric(movies_df['year'], errors='coerce')

            # Calcula o intervalo da década
            start_year = int(decade)
            end_year = start_year + 9

            # Filtra os filmes pela década selecionada
            filtered_movies_by_decade = movies_df[(movies_df['year'] >= start_year) & (movies_df['year'] <= end_year)]

            if not filtered_movies_by_decade.empty:
                print(f"Filmes encontrados para a década de {decade}:")
                print(filtered_movies_by_decade[['title', 'year']])  # Exibe título e ano
                return filtered_movies_by_decade  # Retorna os filmes filtrados
            else:
                print(f"Nenhum filme encontrado para a década de {decade}.")
                return None
        except FileNotFoundError:
            print("Erro: O arquivo do dataset não foi encontrado.")
            return None
        except Exception as e:
            print(f"Ocorreu um erro ao buscar filmes: {e}")
            return None