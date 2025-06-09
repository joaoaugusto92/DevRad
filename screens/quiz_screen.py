import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style, Meter
import config
from data.players_db import update_score, get_ranking

class QuizScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Usa o style criado no app principal
        self.style = controller.style
        self.style.configure('TButton', font=('Arial', 18))
        self.style.configure('TRadiobutton', font=('Arial', 18))
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
        self.quiz_frame.pack(fill='both', expand=True, padx=40, pady=30)
        self._show_question()

    def _show_question(self):
        for w in self.quiz_frame.winfo_children():
            w.destroy()

        # Top bar: Sair e Pontuação
        top_bar = ttk.Frame(self.quiz_frame)
        top_bar.pack(fill='x', pady=(0, 10))
        ttk.Button(
            top_bar,
            text='Sair',
            command=self._exit_quiz,
            style='danger.TButton',
            width=10
        ).pack(side='right', padx=10)
        ttk.Label(
            top_bar,
            text=f'Pontuação: {self.score}',
            font=('Arial', 22, 'bold'),
            foreground='#0d6efd'
        ).pack(side='left', padx=10)

        # Timer circular centralizado
        timer_frame = ttk.Frame(self.quiz_frame)
        timer_frame.pack(pady=(0, 20))
        self.time_elapsed = 0
        self.timer = Meter(
            timer_frame,
            amounttotal=config.TIME_LIMIT,
            amountused=0,
            metersize=120,
            bootstyle='info',
        )
        self.timer.pack()
        self.call_id = self.after(1000, self._update_timer)

        # Pergunta
        q = self.QUESTIONS[self.current_question]
        ttk.Label(
            self.quiz_frame,
            text=f'Pergunta {self.current_question + 1} de {len(self.QUESTIONS)}',
            font=('Arial', 18, 'italic'),
            foreground='#6c757d'
        ).pack(pady=(10, 0))
        ttk.Label(
            self.quiz_frame,
            text=q['question'],
            wraplength=config.APP_WIDTH,
            font=('Arial', 30, 'bold'),
            foreground="#FFFFFF"  # Cor branca para maior contraste
        ).pack(pady=(10, 20))  # Reduzi o espaçamento inferior

        # Opções de resposta
        self.selected_option = tk.IntVar(value=-1)
        self.options_frame = ttk.Frame(self.quiz_frame)
        self.options_frame.pack(pady=(0, 10))  # Menor espaçamento abaixo das opções

        for idx, opt in enumerate(q['options']):
            ttk.Radiobutton(
                self.options_frame,
                text=opt,
                variable=self.selected_option,
                value=idx,
                style='info.TRadiobutton',
                padding=10
            ).pack(anchor='w', padx=30, pady=2)  # Reduzi o pady para 2

        # Botão de enviar
        self.submit_btn = ttk.Button(
            self.quiz_frame,
            text='Enviar',
            style='success.TButton',
            width=18,
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
            result_text, result_style, color = 'Não respondida', 'warning.TLabel', '#ffc107'
        elif choice == q['answer']:
            self.correct += 1
            self.score += 10
            result_text, result_style, color = 'Correta!', 'success.TLabel', '#198754'
        else:
            self.incorrect += 1
            result_text, result_style, color = 'Incorreta!', 'danger.TLabel', '#dc3545'

        # Feedback visual grande e colorido
        feedback = ttk.Label(
        self.quiz_frame,
        text=result_text,
        style=result_style,
        font=('Arial', 28, 'bold'),
        foreground=color,
        anchor='center',
        justify='center'
    ).pack(pady=0, fill="x", expand=True)

        for child in self.options_frame.winfo_children():
            child.configure(state='disabled')
        self.submit_btn.configure(state='disabled')

        self.after(1800, self._next_question)

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
                   command=lambda: self.controller.show_frame('QuizStartScreen')).pack(side='left', padx=20)
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
