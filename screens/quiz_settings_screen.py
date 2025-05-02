import tkinter as tk
from tkinter import ttk
import config

# lista de temas suportados pelo ttkbootstrap
AVAILABLE_THEMES = [
    'cosmo', 'cyborg', 'darkly', 'flatly', 'journal',
    'litera', 'lumen', 'minty', 'morph', 'pulse', 'sandstone',
    'simplex', 'solar', 'superhero', 'united', 'vapor', 'yeti'
]


COMMON_RESOLUTIONS = [
    (800, 600), (1024, 768), (1280, 720), (1920, 1080), "Custom"
]

class QuizSettingsScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.time_limit = tk.IntVar(value=config.TIME_LIMIT)
        self.theme_var = tk.StringVar(value=config.BOOTSTRAP_THEME)
        self.app_width = tk.IntVar(value=config.APP_WIDTH)
        self.app_height = tk.IntVar(value=config.APP_HEIGHT)
        self.resolution_var = tk.StringVar(value=f"{config.APP_WIDTH}x{config.APP_HEIGHT}")
        self.previous_theme = config.BOOTSTRAP_THEME

        ttk.Label(self, text="Configurações do Quiz", font=("Arial", 24)).pack(pady=20)

        # tempo por pergunta
        frm = ttk.Frame(self)
        frm.pack(pady=10)
        ttk.Label(frm, text="Tempo por pergunta (seg):").grid(row=0, column=0, sticky="w")
        ttk.Entry(frm, textvariable=self.time_limit, width=5).grid(row=0, column=1, padx=5)

        # seleção de tema
        ttk.Label(self, text="Tema da aplicação:").pack(pady=(20, 5))
        theme_combobox = ttk.Combobox(self, values=AVAILABLE_THEMES, textvariable=self.theme_var, state="readonly")
        theme_combobox.pack()
        theme_combobox.bind("<<ComboboxSelected>>", self._preview_theme)

        # resolução do aplicativo
        ttk.Label(self, text="Resolução do aplicativo:").pack(pady=(20, 5))
        res_frame = ttk.Frame(self)  # ⬅ parent correto
        res_frame.pack()

        # monta a lista de resoluções: '800x600', '1024x768', ..., 'Custom'
        res_list = [
            f"{res[0]}x{res[1]}" if isinstance(res, tuple) else res
            for res in COMMON_RESOLUTIONS
        ]
        ttk.Label(res_frame, text="Resolução:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.resolution_combobox = ttk.Combobox(
            res_frame,                   # ⬅ parent correto
            values=res_list,
            textvariable=self.resolution_var,
            state="readonly"
        )
        self.resolution_combobox.grid(row=0, column=1, columnspan=3, sticky="w", padx=5, pady=(0, 5))
        self.resolution_combobox.bind("<<ComboboxSelected>>", self._update_resolution_fields)

        ttk.Label(res_frame, text="Largura:").grid(row=1, column=0, sticky="w")
        self.width_entry = ttk.Entry(res_frame, textvariable=self.app_width, width=5, state="disabled")
        self.width_entry.grid(row=1, column=1, padx=5)
        ttk.Label(res_frame, text="Altura:").grid(row=1, column=2, sticky="w")
        self.height_entry = ttk.Entry(res_frame, textvariable=self.app_height, width=5, state="disabled")
        self.height_entry.grid(row=1, column=3, padx=5)

        # botões
        btns = ttk.Frame(self)
        btns.pack(pady=20)
        ttk.Button(btns, text="Salvar", command=self._apply).grid(row=0, column=0, padx=10)
        ttk.Button(btns, text="Voltar", command=self._cancel).grid(row=0, column=1)

    def _preview_theme(self, event):
        """Aplica o tema selecionado temporariamente."""
        from ttkbootstrap import Style
        self.controller.style = Style(self.theme_var.get())

    def _update_resolution_fields(self, event):
        """Atualiza os campos de largura e altura com base na seleção de resolução."""
        selected = self.resolution_var.get()
        if selected == "Custom":
            self.width_entry.config(state="normal")
            self.height_entry.config(state="normal")
        else:
            self.width_entry.config(state="disabled")
            self.height_entry.config(state="disabled")
            width, height = map(int, selected.split("x"))
            self.app_width.set(width)
            self.app_height.set(height)

    def _apply(self):
        # atualiza config
        config.TIME_LIMIT = self.time_limit.get()
        config.BOOTSTRAP_THEME = self.theme_var.get()
        config.APP_WIDTH = self.app_width.get()
        config.APP_HEIGHT = self.app_height.get()

        # reaplica o tema em todo o app
        from ttkbootstrap import Style
        self.controller.style = Style(config.BOOTSTRAP_THEME)

        # atualiza a resolução do app
        self.controller.geometry(f"{config.APP_WIDTH}x{config.APP_HEIGHT}")

        # volta ao menu
        self.controller.show_frame("InitialScreen")

    def _cancel(self):
        """Reverte o tema para o anterior e volta ao menu inicial."""
        from ttkbootstrap import Style
        self.controller.style = Style(self.previous_theme)
        self.controller.show_frame("InitialScreen")