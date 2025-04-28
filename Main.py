#Importando as bibliotecas usadas(tkinter e pandas)
import tkinter as tk
import pandas as pd

#Criando a função que vai limpar a tela atual
def limpar_tela():
    #Utilizando um laço de repetição que vai passar por todos os itens na janela
    for widget in root.winfo_children():
        #Comando que vai apagar todos os itens na tela
        widget.destroy()

#Crindo a função que quando for chamada vai limpar a tela atual e mostrar a tela de menu
def mostrar_menu():
    #Chamando a função de limpar a tela
    limpar_tela()

    #Colocando um titulo na tela e posicionando em pillha
    tk.Label(root, text="Quiz de Filmes",font=('Arial', 18)).pack(pady=10)
    #Criando um botão que quando apertado vai chamar a função de iniciar o quiz
    tk.Button(root,text="Iniciar Quiz").pack(pady=10)
    #Criaando um botão que quando apertado vai chamar a função de mostrar a tela de pesquisa
    tk.Button(root,text = "Pesquisar Filmes",command=mostrar_tela_pesquisa).pack()
    #Criando um botão que quando apertado vai encerrar o loop da janela(fechando a janela)
    tk.Button(root, text="Sair", command=root.quit).pack(pady=10)



# Criando a função que ira trocar da tela para a tela de pesquisa
def mostrar_tela_pesquisa():
    limpar_tela()  # Função que limpa a tela anterior

    #Declarando a variavel global para armazenar o campo de entrada
    global entry_keywords

    # Criando um titulo
    tk.Label(root, text="Saiba mais sobre seu filme favorito", font=('Arial', 18)).pack(pady=10)

    # Criando um campo de entrada onde o que for digitado sera armazenado na variavel global entry_keywords
    entry_keywords = tk.Entry(root, width=50)
    # Colocando um texto dentro do campo de pesquisa,para instruir o usuario
    entry_keywords.insert(0, "Digite o titulo do filme(em inglês)")
    # Posicionando o campo de entrada em estrutura de pilha na tela
    entry_keywords.pack(pady=5)

    # Criando um botão que irá chamar a função de pesquisar um filme dentro do database
    tk.Button(root, text="Pesquisar Filme",command=pesquisar_filme).pack()
    # Criando um botão que volta ao menu quando apertado
    tk.Button(root, text="Voltar ao Menu", command=mostrar_menu).pack(pady=10)

    # Quando o campo recebe foco chama a função de apagar o texto que estava no campo de entrada
    entry_keywords.bind("<FocusIn>", on_entry_click)



# Criando a função que vai apagar o texto no campo de entrada quando o usuario clicar(der foco) nele
def on_entry_click(event):
    global entry_keywords

    #Criando a condição que quando for atendida vai apagar a mensagem no campo de entrada
    if entry_keywords.get() == "Digite o titulo do filme(em inglês)":
        entry_keywords.delete(0, tk.END)  # Limpa o campo
        entry_keywords.config(fg="black")  # Muda a cor do texto

#Criando a função para pesquisar filmes no database a partir de palavras chave do seu titulo
def pesquisar_filme():
    #Chamando a variavel global que esta armazenando o campo de entrada
    global entry_keywords
    #Criando uma variavel para armazenar o que o usuario digitou utilizando o metodo get e deixando todas as letras minusculas
    pesquisa = entry_keywords.get().strip().lower()

    #Utilizando try exept para tratamento de erros
    try:
        #Vinculando o arquivo csv ao codigo utilizando a biblioteca pandas
        df = pd.read_csv("DataSet/world_imdb_movies_top_movies_per_year.csv", sep=",", encoding="utf-8")
        # Cria uma variável que armazena os filmes cujo título contém todas as palavras digitadas na pesquisa
        resultados = df[df["title"].str.lower().apply(lambda x: all(word in x for word in pesquisa.split()))]

        #Chamando a função para limpar a tela atual
        limpar_tela()

        # Cria o frame principal da tela de resultados
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        #Criando um titulo para a pagina de resultados
        tk.Label(main_frame, text="Resultados da Pesquisa:", font=('Arial', 14, 'bold')).pack(pady=10)

        # Cria o canvas e a barra de rolagem vertical
        canvas = tk.Canvas(main_frame)
        scrollbar = tk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas)

        # Configura o canvas para atualizar a área rolável conforme o tamanho do conteúdo
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        # Adiciona o frame rolável dentro do canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Habilita o uso da roda do mouse para rolar o conteúdo
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        # Associa o evento da roda do mouse ao canvas
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # Posiciona o canvas e a barra de rolagem na tela
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        #Criando a condição que vai mostrar os resultados encontrados(Caso tenham)
        if not resultados.empty:
            #Percorre os filmes encontrados e exibe seus dados formatados
            for i, (_, filme) in enumerate(resultados.iterrows()):
                #Formata as informações do filme em uma string
                filme_str = (f"Título: {filme['title']}\nAno: {filme['year']}\nGênero: {filme['genre']}\nDuração:{filme['duration']}\n"
                             f"Oscar:{filme['oscar']}\nNota IMDB:{filme['rating_imdb']}")
                tk.Label(scrollable_frame,
                         text=filme_str,
                         font=('Arial', 10),
                         anchor='w',
                         justify='left').pack(fill='x', padx=20, pady=2)

                tk.Frame(scrollable_frame, height=1, bg='lightgray').pack(fill='x', padx=20)
        #Exibe uma mensagem caso o filme não tenha sido encontrado
        else:
            tk.Label(scrollable_frame,
                     text=f"Nenhum filme encontrado com: '{pesquisa}'", fg="red").pack(pady=20)

        # Cria um frame para conter os botões de navegação
        button_frame = tk.Frame(scrollable_frame)
        button_frame.pack(pady=20)

        #Criando os botões que podem ser clicados para realizar uma nova pesquisa ou voltar ao menu incial
        tk.Button(button_frame, text="Nova Pesquisa", command=mostrar_tela_pesquisa).pack(side='left', padx=10)
        tk.Button(button_frame, text="Menu Principal", command=mostrar_menu).pack(side='left', padx=10)

    #Caso o programa de algum erro uma mensagem aparecera na tela
    except Exception as e:
        tk.Label(main_frame, text=f"Erro: {str(e)}", fg="red").pack()



#Criando a janela principal do codigo e deixando ela em loop
root = tk.Tk()
root.geometry("500x400")
mostrar_menu()

root.mainloop()