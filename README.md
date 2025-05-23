# DevRad – DashMovies

Uma aplicação desktop em Python/Tkinter estilizada com **ttkbootstrap**, que combina funcionalidades de busca de filmes e quiz interativo.

---

## 🗂️ Estrutura de Pastas

```
DevRad/
├── .git/
├── .gitignore
├── DataSet/
│   └── world_imdb_movies_top_movies_per_year.csv  # Dados CSV externos (não versionados)
├── data/
│   └── questions.py       # Lógica de geração dinâmica de perguntas
├── screens/
│   ├── initial_screen.py
│   ├── movie_search_screen.py
│   ├── quiz_settings_screen.py
│   ├── quiz_start_screen.py
│   └── quiz_screen.py
├── services/
│   └── moviesService.py   # Interfaces de busca e filtragem de filmes
├── config.py              # Configurações globais (tema, tempo, resolução)
├── Main.py                # Ponto de entrada da aplicação e controle de telas
├── requirements.txt       # Dependências
└── README.md              # Este arquivo (atualizado)
```

---

## 🔍 Funcionalidades Atuais

1. **Busca de Filmes**

   * Carrega o CSV `world_imdb_movies_top_movies_per_year.csv` (coloque-o dentro da pasta `DataSet`).
   * Filtros por palavra-chave no título (em inglês), gênero e década.
   * Ordenação por bilheteria mundial e formatação em K/M/B.
   * Exibição responsiva com canvas rolável e paginação.

2. **Quiz Interativo**

   * Tela de configuração de filtros (gênero e década).
   * Geração dinâmica de 5 perguntas (`get_questions`), sorteando 5 filmes e criando opções de ano correto/incorreto.
   * Timer visual com componente `Meter` do **ttkbootstrap**, configurável via `config.TIME_LIMIT`.
   * Feedback imediato por resposta (Correta, Incorreta, Não respondida).
   * Resumo final com estatísticas de pontuação, acertos, erros e não respondidas.

3. **Configurações Dinâmicas**

   * Ajuste de **temas** (mais de 16 temas disponíveis em **ttkbootstrap**).
   * Definição de **tempo por pergunta** (em segundos).
   * Ajuste de **resolução** da janela (predefinidas ou customizada).
   * Alterações aplicadas em tempo real e mantidas durante a sessão.

---

## 🚀 Como Executar

1. **Clone** este repositório:

   ```bash
   git clone <URL-do-repositório>
   cd DevRad
   ```

2. **Crie** um ambiente virtual (recomendado):

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Linux/macOS
   .venv\Scripts\activate     # Windows
   ```

3. **Instale** as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. **Garanta** que o arquivo CSV `world_imdb_movies_top_movies_per_year.csv` esteja em `DataSet/`.

5. **Execute** o aplicativo:

   ```bash
   python Main.py
   ```

---

## 🛠️ Configurações (config.py)

* `TIME_LIMIT`: segundos para cada pergunta (padrão: 10).
* `BOOTSTRAP_THEME`: tema inicial do **ttkbootstrap** (padrão: `darkly`).
* `APP_WIDTH`, `APP_HEIGHT`: resolução da janela.

Todas as configurações podem ser ajustadas em tempo real na tela de "Configurações".

---

## 📈 Próximos Passos / Roadmap

* **Persistência de Configurações**: salvar configurações do usuário em JSON para recarregar na próxima sessão.
