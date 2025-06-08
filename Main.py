import tkinter as tk
from ttkbootstrap import Style
import config
from data.players_db import init_db

# Inicializa o banco de dados ANTES de importar as telas
init_db()

from screens.login_screen import LoginScreen
from screens.ranking_screen import RankingScreen
from screens.initial_screen import InitialScreen
from screens.movie_search_screen import MovieSearchScreen
from screens.quiz_settings_screen import QuizSettingsScreen
from screens.quiz_start_screen import QuizStartScreen
from screens.quiz_screen import QuizScreen
from screens.admin_players_screen import AdminPlayersScreen


class QuizApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DashMovies")
        self.geometry(f"{config.APP_WIDTH}x{config.APP_HEIGHT}")



        # cria o Style uma única vez, usando o tema do config
        self.style = Style(config.BOOTSTRAP_THEME)
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (
            LoginScreen,
            InitialScreen,
            MovieSearchScreen,
            QuizSettingsScreen,
            QuizStartScreen,
            QuizScreen,
            RankingScreen,
            AdminPlayersScreen
        ):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("InitialScreen")

    def show_frame(self, name: str):
        frame = self.frames[name]
        # Chama on_show se existir
        if hasattr(frame, "on_show"):
            frame.on_show()
        frame.tkraise()

if __name__ == "__main__":
    app = QuizApp()
    app.mainloop()