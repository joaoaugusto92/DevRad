import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style, Meter
import config
from data.players_db import update_score, get_ranking

class QuizScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # use o style criado no app principal
        self.style = controller.style
        self.style.configure('TButton', font=('Arial', 16))
        self.call_id = None

    def _exit_quiz(self):
        if self.call_id:
            self.after_cancel(self.call_id)
            self.call_id = None
        self.controller.show_frame('InitialScreen')

    def start_quiz(self, QUESTIONS):
        self.QUESTIONS = QUESTIONS
        self.current_question = 0
        self.score = 0
        self.correct = 0
        self.incorrect = 0
        self.unattempted = 0

        for w in self.winfo_children():
            w.destroy()

        self.quiz_frame = ttk.Frame(self)
        self.quiz_frame.pack(fill='both', expand=True)
        self._show_question()

    def _show_question(self):
        for w in self.quiz_frame.winfo_children():
            w.destroy()

        exit_btn = ttk.Button(
            self.quiz_frame,
            text='Sair',
            command=self._exit_quiz,
            style='TButton'
        )
        exit_btn.pack(anchor='ne', padx=10, pady=5)

        ttk.Label(
            self.quiz_frame,
            text=f'Pontuação: {self.score}',
            font=('Arial', 28)
        ).pack(anchor='nw', padx=10, pady=10)

        self.time_elapsed = 0
        self.timer = Meter(
            self.quiz_frame,
            amounttotal=config.TIME_LIMIT,
            amountused=0,
            metersize=100,
            bootstyle='info'
        )
        self.timer.pack(anchor='ne', padx=10, pady=10)
        self.call_id = self.after(1000, self._update_timer)

        q = self.QUESTIONS[self.current_question]
        ttk.Label(
            self.quiz_frame,
            text=q['question'],
            wraplength=600,
            font=('Arial', 32)
        ).pack(pady=20)

        self.selected_option = tk.IntVar(value=-1)
        self.options_frame = ttk.Frame(self.quiz_frame)
        self.options_frame.pack()

        self.style.configure('TRadiobutton', font=('Arial', 18))

        for idx, opt in enumerate(q['options']):
            ttk.Radiobutton(
                self.options_frame,
                text=opt,
                variable=self.selected_option,
                value=idx,
                style='TRadiobutton'
            ).pack(anchor='w', padx=20, pady=5)

        self.submit_btn = ttk.Button(
            self.quiz_frame,
            text='Enviar',
            command=self._submit_answer
        )
        self.submit_btn.pack(pady=20)

    def _update_timer(self):
        self.time_elapsed += 1
        self.timer.configure(amountused=self.time_elapsed)
        if self.time_elapsed < config.TIME_LIMIT:
            self.call_id = self.after(1000, self._update_timer)
        else:
            self._submit_answer()

    def _submit_answer(self):
        if self.call_id:
            self.after_cancel(self.call_id)
            self.call_id = None

        q = self.QUESTIONS[self.current_question]
        choice = self.selected_option.get()

        if choice == -1:
            self.unattempted += 1
            result_text, result_style = 'Não respondida', 'warning.TLabel'
        elif choice == q['answer']:
            self.correct += 1
            self.score += 10
            result_text, result_style = 'Correta', 'success.TLabel'
        else:
            self.incorrect += 1
            result_text, result_style = 'Incorreta', 'danger.TLabel'

        ttk.Label(
            self.quiz_frame,
            text=result_text,
            style=result_style,
            font=('Arial', 32)
        ).pack()

        for child in self.options_frame.winfo_children():
            child.configure(state='disabled')
        self.submit_btn.configure(state='disabled')

        self.after(2000, self._next_question)

    def _next_question(self):
        self.current_question += 1
        if self.current_question < len(self.QUESTIONS):
            self._show_question()
        else:
            self._show_summary()

    def _show_summary(self):
        # Limpa a tela do quiz
        for w in self.quiz_frame.winfo_children():
            w.destroy()

        total = len(self.QUESTIONS)
        acertos = self.correct
        erros = self.incorrect
        score = self.score

        # Salva a pontuação se estiver logado
        if hasattr(self.controller, "current_user") and self.controller.current_user:
            player_id = self.controller.current_user[0]
            update_score(player_id, score)

        # Mensagem motivacional
        if acertos >= total * 0.7:
            msg = "🎉 Parabéns! Você foi muito bem! Continue jogando para melhorar ainda mais seu ranking!"
            msg_style = "success.TLabel"
        elif acertos > 0:
            msg = "👏 Bom esforço! Continue jogando para melhorar sua pontuação e subir no ranking!"
            msg_style = "info.TLabel"
        else:
            msg = "Não desanime! Continue jogando para melhorar sua pontuação e subir no ranking!"
            msg_style = "warning.TLabel"

        ttk.Label(
            self.quiz_frame,
            text=msg,
            style=msg_style,
            wraplength=600,
            justify="center",
            font=("Arial", 18, "bold")  
        ).pack(pady=(20, 10))

        # Resumo do quiz
        ttk.Label(self.quiz_frame, text='Resumo do Quiz', font=("Arial", 24, "bold")).pack(pady=10)
        ttk.Label(self.quiz_frame, text=f'Total de perguntas: {total}', font=("Arial", 14)).pack(pady=2)
        ttk.Label(self.quiz_frame, text=f'Pontuação: {score}', font=("Arial", 16, "bold")).pack(pady=2)
        ttk.Label(self.quiz_frame, text=f'Corretas: {acertos}', font=("Arial", 14)).pack(pady=2)
        ttk.Label(self.quiz_frame, text=f'Incorretas: {erros}', font=("Arial", 14)).pack(pady=2)
        ttk.Label(self.quiz_frame, text=f'Não respondidas: {self.unattempted}', font=("Arial", 14)).pack(pady=2)

        # Botões
        btn_frame = ttk.Frame(self.quiz_frame)
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text='Jogar Novamente', style="success.TButton", width=20,
                   command=lambda: self.start_quiz(self.QUESTIONS)).pack(side='left', padx=20)
        ttk.Button(btn_frame, text='Voltar ao Menu', style="secondary.TButton", width=20,
                   command=lambda: self.controller.show_frame('InitialScreen')).pack(side='right', padx=20)

        # Cadastro ou mensagem de login
        if not hasattr(self.controller, "current_user") or not self.controller.current_user:
            ttk.Label(self.quiz_frame, text="Cadastre-se para ver seu ranking e guardar seus pontos!",
                      font=("Arial", 12)).pack(pady=(30, 5))
            ttk.Button(self.quiz_frame, text="Cadastre-se", style="info.TButton", width=16,
                       command=lambda: self.controller.show_frame("LoginScreen")).pack()
        else:
            ttk.Label(self.quiz_frame, text="Sua pontuação foi salva! Continue jogando para subir no ranking.",
                      font=("Arial", 12)).pack(pady=(30, 5))

        # --- Ranking dos jogadores ---
        ttk.Label(self.quiz_frame, text="Ranking dos Jogadores", font=("Arial", 20, "bold")).pack(pady=(30, 10))
        tree = ttk.Treeview(self.quiz_frame, columns=("Nome", "Pontuação"), show="headings", height=10)
        tree.heading("Nome", text="Nome")
        tree.heading("Pontuação", text="Pontuação")
        tree.pack(padx=20, pady=10, fill="x")

        # Atualiza e insere os dados do ranking
        for row in tree.get_children():
            tree.delete(row)
        for nome, pontuacao in get_ranking():
            tree.insert("", "end", values=(nome, pontuacao))