import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style, Meter
import config

class QuizScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # use o style criado no app principal
        self.style = controller.style
        self.style.configure('TButton', font=('Arial', 16))
        self.call_id = None

    def _exit_quiz(self):
        """Encerra o quiz imediatamente e volta ao menu principal."""
        if self.call_id:
            self.after_cancel(self.call_id)
            self.call_id = None
        self.controller.show_frame('InitialScreen')

    def start_quiz(self, QUESTIONS):
        self.QUESTIONS = QUESTIONS
        """
        Inicializa ou reinicia o quiz: zera o placar e exibe a primeira pergunta.
        """
        # Estado inicial
        self.current_question = 0
        self.score = 0
        self.correct = 0
        self.incorrect = 0
        self.unattempted = 0

        # Limpa tela
        for w in self.winfo_children():
            w.destroy()

        # Container das perguntas
        self.quiz_frame = ttk.Frame(self)
        self.quiz_frame.pack(fill='both', expand=True)

        # Mostra a primeira pergunta
        self._show_question()

    def _show_question(self):
        # Limpa widgets anteriores
        for w in self.quiz_frame.winfo_children():
            w.destroy()

        # Botão de sair do quiz a qualquer momento
        exit_btn = ttk.Button(
            self.quiz_frame,
            text='Sair',
            command=self._exit_quiz,
            style='TButton'
        )
        exit_btn.pack(anchor='ne', padx=10, pady=5)

        # Exibe placar
        ttk.Label(
            self.quiz_frame,
            text=f'Pontuação: {self.score}',
            font=('Arial', 28)
        ).pack(anchor='nw', padx=10, pady=10)

        # Timer circular
        self.time_elapsed = 0
        self.timer = Meter(
            self.quiz_frame,
            amounttotal=config.TIME_LIMIT,
            amountused=0,
            metersize=100,
            bootstyle='info'
        )
        self.timer.pack(anchor='ne', padx=10, pady=10)
        # Inicia contagem
        self.call_id = self.after(1000, self._update_timer)

        # Carrega pergunta atual
        q = self.QUESTIONS[self.current_question]
        ttk.Label(
            self.quiz_frame,
            text=q['question'],
            wraplength=600,
            font=('Arial', 32)
        ).pack(pady=20)

        # Opções de resposta
        self.selected_option = tk.IntVar(value=-1)
        self.options_frame = ttk.Frame(self.quiz_frame)
        self.options_frame.pack()

        # Ajuste de estilo para radio buttons usando o Style do ttkbootstrap
        self.style.configure('TRadiobutton', font=('Arial', 18))

        for idx, opt in enumerate(q['options']):
            ttk.Radiobutton(
                self.options_frame,
                text=opt,
                variable=self.selected_option,
                value=idx,
                style='TRadiobutton'
            ).pack(anchor='w', padx=20, pady=5)

        # Botão de enviar
        self.submit_btn = ttk.Button(
            self.quiz_frame,
            text='Enviar',
            command=self._submit_answer
        )
        self.submit_btn.pack(pady=20)

    def _update_timer(self):
        """Atualiza o medidor de tempo a cada segundo."""
        self.time_elapsed += 1
        self.timer.configure(amountused=self.time_elapsed)
        if self.time_elapsed < config.TIME_LIMIT:
            self.call_id = self.after(1000, self._update_timer)
        else:
            self._submit_answer()

    def _submit_answer(self):
        """Processa a resposta, exibe feedback e segue para a próxima pergunta."""
        # Cancela contagem do timer
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

        # Feedback na tela
        ttk.Label(
            self.quiz_frame,
            text=result_text,
            style=result_style,
            font=('Arial', 32)
        ).pack()

        # Desabilita interações
        for child in self.options_frame.winfo_children():
            child.configure(state='disabled')
        self.submit_btn.configure(state='disabled')

        # Avança após 2 segundos
        self.after(2000, self._next_question)

    def _next_question(self):
        """Mostra a próxima pergunta ou resumo final."""
        self.current_question += 1
        if self.current_question < len(self.QUESTIONS):
            self._show_question()
        else:
            self._show_summary()

    def _show_summary(self):
        """Exibe o resumo do quiz com estatísticas e opções de reinício ou saída."""
        # Limpa tela
        for w in self.quiz_frame.winfo_children():
            w.destroy()

        ttk.Label(
            self.quiz_frame,
            text='Resumo do Quiz',
            font=('Arial', 40)
        ).pack(pady=20)
        ttk.Label(
            self.quiz_frame,
            text=f'Total: {len(self.QUESTIONS)}   Pontuação: {self.score}',
            font=('Arial', 28)
        ).pack(pady=5)
        ttk.Label(
            self.quiz_frame,
            text=f'Corretas: {self.correct}',
            style='success.TLabel',
            font=('Arial', 28)
        ).pack(pady=5)
        ttk.Label(
            self.quiz_frame,
            text=f'Incorretas: {self.incorrect}',
            style='danger.TLabel',
            font=('Arial', 28)
        ).pack(pady=5)
        ttk.Label(
            self.quiz_frame,
            text=f'Não respondidas: {self.unattempted}',
            style='warning.TLabel',
            font=('Arial', 28)
        ).pack(pady=5)

        # Botões de ação
        btn_frame = ttk.Frame(self.quiz_frame)
        btn_frame.pack(pady=20)
        ttk.Button(
            btn_frame,
            text='Jogar Novamente',
            command=self.start_quiz
        ).pack(side='left', padx=20)
        ttk.Button(
            btn_frame,
            text='Voltar ao Menu',
            command=lambda: self.controller.show_frame('InitialScreen')
        ).pack(side='right', padx=20)
