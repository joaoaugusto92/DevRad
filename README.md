# DevRad – DashMovies

Uma aplicação desktop em Python/Tkinter estilizada com **ttkbootstrap**, que combina duas funcionalidades principais:

## Descrição

**DevRad – DashMovies** oferece ao usuário:

1. **Busca de Filmes**

   * Carrega um dataset CSV (`world_imdb_movies_top_movies_per_year.csv`).
   * Permite pesquisar por palavras-chave no título (em inglês).
   * Exibe resultados ordenados por bilheteria mundial, formatados em K, M, B.
   * Interface responsiva com canvas rolável para navegação dos resultados.

2. **Quiz sobre Filmes**

   * Quiz de múltipla escolha com perguntas estáticas e futura geração dinâmica por década/gênero.
   * Timer circular configurável (padrão 10 segundos) usando o componente `Meter` do ttkbootstrap.
   * Feedback imediato (Correta, Incorreta, Não respondida) e resumo final com estatísticas (pontuação, acertos, erros, não respondidas).

3. **Tela de Configurações**

   * Ajuste de tempo por pergunta.
   * Escolha de tema (vários temas ttkbootstrap).
   * Definição de resolução da janela (padrões ou customizada).

## Estrutura de Pastas

```
DevRad/
├── .git/
├── data/
│   └── questions.py       # Perguntas estáticas do quiz
├── screens/
│   ├── initial_screen.py
│   ├── movie_search_screen.py
│   ├── quiz_settings_screen.py
│   ├── quiz_start_screen.py
│   └── quiz_screen.py
├── .gitignore
├── config.py              # Configurações globais de tema, tempo, resolução
├── main.py                # Inicialização da aplicação e controle de telas
└── requirements.txt       # Dependências do projeto
```

## Funcionalidades Principais

* **Navegação entre telas**: Menu inicial, busca de filmes, quiz, configurações.
* **Pesquisa de Filmes**: Campo de texto com placeholder, pesquisa via pandas, exibição rolável.
* **Quiz Interativo**: Contagem regressiva visual, feedback de respostas, estatísticas finais.
* **Configurações Dinâmicas**: Alteração de tema, tempo e resolução com preview e persistência.

## Instalação

1. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```
2. Execute a aplicação:

   ```bash
   python main.py
   ```

## Uso

* **Busca de Filmes**: Digite trecho do título (inglês) e clique em “Pesquisar Filme”.
* **Quiz**: Selecione “Quiz” no menu, configure tempo/tema se desejar, inicie o quiz.
* **Configurações**: Ajuste tempo por pergunta, tema e resolução; salve para aplicar.

## Próximos Passos / Roadmap

* **Persistência de Configurações**: Armazenar em arquivo JSON em vez de variáveis globais.
* **Filtros Avançados na Busca**: Filtros por gênero e faixa de ano.
* **Geração Dinâmica de Perguntas**: Quiz baseado em dados reais do CSV (décadas, gêneros).
