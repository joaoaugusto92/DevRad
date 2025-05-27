import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style, Meter
import config
from ui.widgets import StyledButton, StyledLabel

class QuizScreen(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.style = controller.style
        self.call_id = None
        self.configure(style='Quiz.TFrame')

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
        exit_btn = StyledButton(
            self.quiz_frame,
            text='Sair',
            command=self._exit_quiz,
            bootstyle='danger',
        )
        exit_btn.pack(anchor='ne', padx=config.PADDING_DEFAULT, pady=config.PADDING_DEFAULT)

        # Exibe placar
        StyledLabel(
            self.quiz_frame,
            text=f'Pontuação: {self.score}',
            font=(config.FONT_FAMILY, config.FONT_SIZE_SUBTITLE),
            foreground=config.COLOR_PRIMARY,
        ).pack(anchor='nw', padx=config.PADDING_DEFAULT, pady=config.PADDING_DEFAULT)

        # Timer circular
        self.time_elapsed = 0
        self.timer = Meter(
            self.quiz_frame,
            amounttotal=config.TIME_LIMIT,
            amountused=0,
            metersize=100,
            bootstyle='info'
        )
        self.timer.pack(anchor='ne', padx=config.PADDING_DEFAULT, pady=config.PADDING_DEFAULT)
        # Inicia contagem
        self.call_id = self.after(1000, self._update_timer)

        # Carrega pergunta atual
        q = self.QUESTIONS[self.current_question]
        StyledLabel(
            self.quiz_frame,
            text=q['question'],
            wraplength=600,
            font=(config.FONT_FAMILY, config.FONT_SIZE_TITLE),
            foreground=config.COLOR_PRIMARY,
        ).pack(pady=config.PADDING_LARGE)

        # Opções de resposta
        self.selected_option = tk.IntVar(value=-1)
        self.options_frame = ttk.Frame(self.quiz_frame)
        self.options_frame.pack()

        for idx, opt in enumerate(q['options']):
            ttk.Radiobutton(
                self.options_frame,
                text=opt,
                variable=self.selected_option,
                value=idx,
                style='TRadiobutton'
            ).pack(anchor='w', padx=config.PADDING_LARGE, pady=config.PADDING_DEFAULT)

        # Botão de enviar
        self.submit_btn = StyledButton(
            self.quiz_frame,
            text='Enviar',
            command=self._submit_answer,
            bootstyle='primary',
        )
        self.submit_btn.pack(pady=config.PADDING_LARGE)

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
            result_text, result_style, color = 'Não respondida', 'warning.TLabel', config.COLOR_WARNING
        elif choice == q['answer']:
            self.correct += 1
            self.score += 10
            result_text, result_style, color = 'Correta', 'success.TLabel', config.COLOR_SUCCESS
        else:
            self.incorrect += 1
            result_text, result_style, color = 'Incorreta', 'danger.TLabel', config.COLOR_DANGER

        # Feedback na tela
        StyledLabel(
            self.quiz_frame,
            text=result_text,
            style=result_style,
            font=(config.FONT_FAMILY, config.FONT_SIZE_TITLE),
            foreground=color,
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
        StyledLabel(
            self.quiz_frame,
            text='Resumo do Quiz',
            font=(config.FONT_FAMILY, 40),
            foreground=config.COLOR_PRIMARY,
        ).pack(pady=config.PADDING_LARGE)
        StyledLabel(
            self.quiz_frame,
            text=f'Total: {len(self.QUESTIONS)}   Pontuação: {self.score}',
            font=(config.FONT_FAMILY, config.FONT_SIZE_SUBTITLE),
            foreground=config.COLOR_PRIMARY,
        ).pack(pady=config.PADDING_DEFAULT)
        StyledLabel(
            self.quiz_frame,
            text=f'Corretas: {self.correct}',
            style='success.TLabel',
            font=(config.FONT_FAMILY, config.FONT_SIZE_SUBTITLE),
            foreground=config.COLOR_SUCCESS,
        ).pack(pady=config.PADDING_DEFAULT)
        StyledLabel(
            self.quiz_frame,
            text=f'Incorretas: {self.incorrect}',
            style='danger.TLabel',
            font=(config.FONT_FAMILY, config.FONT_SIZE_SUBTITLE),
            foreground=config.COLOR_DANGER,
        ).pack(pady=config.PADDING_DEFAULT)
        StyledLabel(
            self.quiz_frame,
            text=f'Não respondidas: {self.unattempted}',
            style='warning.TLabel',
            font=(config.FONT_FAMILY, config.FONT_SIZE_SUBTITLE),
            foreground=config.COLOR_WARNING,
        ).pack(pady=config.PADDING_DEFAULT)
        btn_frame = ttk.Frame(self.quiz_frame)
        btn_frame.pack(pady=config.PADDING_LARGE)
        StyledButton(
            btn_frame,
            text='Jogar Novamente',
            command=self.start_quiz,
            bootstyle='primary',
        ).pack(side='left', padx=config.PADDING_LARGE)
        StyledButton(
            btn_frame,
            text='Voltar ao Menu',
            command=lambda: self.controller.show_frame('InitialScreen'),
            bootstyle='secondary',
        ).pack(side='right', padx=config.PADDING_LARGE)
