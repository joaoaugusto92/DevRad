# Widgets customizados com estilos padronizados
from tkinter import ttk
from ttkbootstrap import Entry as _Entry

class StyledButton(ttk.Button):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', 'TButton')
        super().__init__(*args, **kwargs)

class StyledLabel(ttk.Label):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('style', 'TLabel')
        super().__init__(*args, **kwargs)

class StyledEntry(_Entry):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('bootstyle', 'light')
        super().__init__(*args, **kwargs)
