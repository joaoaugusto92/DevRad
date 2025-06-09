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
│   ├── questions.py           # Lógica de geração dinâmica de perguntas
│   ├── players_db.py          # Banco de dados e funções de usuários/jogadores
├── screens/
│   ├── initial_screen.py
│   ├── movie_search_screen.py
│   ├── quiz_settings_screen.py
│   ├── quiz_start_screen.py
│   ├── quiz_screen.py
│   ├── login_screen.py           # Tela de login/cadastro de usuários
│   ├── ranking_screen.py         # Tela de ranking dos jogadores
│   └── admin_players_screen.py   # Tela de administração de jogadores (apenas admin)
├── services/
│   └── moviesService.py       # Interfaces de busca e filtragem de filmes
├── config.py                  # Configurações globais (tema, tempo, resolução)
├── Main.py                    # Ponto de entrada da aplicação e controle de telas
├── requirements.txt           # Dependências
└── README.md                  # Este arquivo (atualizado)
```

## 🔍 Funcionalidades Atuais

1. **Busca de Filmes**

   * Carrega o CSV `world_imdb_movies_top_movies_per_year.csv` (coloque-o dentro da pasta `DataSet`).
   * Filtros por palavra-chave no título (em inglês), gênero e década.
   * Ordenação por bilheteria mundial e formatação em K/M/B.
   * Exibição responsiva com canvas rolável e paginação.

2. **Quiz Interativo**

   * Tela de configuração de filtros (gênero e década).
   * Geração dinâmica de 5 perguntas (`get_questions`), sorteando 5 filmes e criando opções de ano correto/incorreto.
   * **Agora as alternativas de ano respeitam a década escolhida pelo usuário.**
   * Timer visual com componente `Meter` do **ttkbootstrap**, configurável via `config.TIME_LIMIT`.
   * Feedback imediato por resposta (Correta, Incorreta, Não respondida), centralizado e sempre visível.
   * Resumo final com estatísticas de pontuação, acertos, erros e não respondidas, além do ranking dos jogadores.

3. **Configurações Dinâmicas**

   * Ajuste de **temas** (mais de 16 temas disponíveis em **ttkbootstrap**).
   * Definição de **tempo por pergunta** (em segundos).
   * Ajuste de **resolução** da janela (predefinidas ou customizada).
   * Alterações aplicadas em tempo real e mantidas durante a sessão.

4. **Ranking e Administração**

   * Ranking dos jogadores exibido ao final do quiz e em tela própria.
   * **Administrador não aparece mais no ranking.**
   * Tela de administração acessível apenas para usuários com `is_admin=1`.

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

## 🆕 Atualizações Recentes

### [07 e 08/06/2025] Novas Funcionalidades, Telas e Melhorias

- **Novo banco de dados de jogadores (`players_db`):**
  - Cadastro, autenticação e armazenamento de pontuação dos usuários.
  - Suporte a usuários administradores (`is_admin=1`), que podem acessar a tela de administração.

- **Tela de Login e Cadastro:**
  - Usuários podem se cadastrar, fazer login e ter suas pontuações salvas.
  - O campo de login só aparece para quem não está logado.
  - Usuários logados veem mensagem de boas-vindas.

- **Tela de Administração de Jogadores:**
  - Acesso exclusivo para administradores.
  - Permite visualizar, editar e remover jogadores cadastrados.

- **Tela de Ranking:**
  - Exibe o ranking dos jogadores comuns (admin não aparece).
  - Ranking também é mostrado ao final do quiz.

- **Integração entre telas:**
  - Após login, o usuário é redirecionado conforme seu perfil (admin ou jogador).
  - O fluxo de navegação entre as telas foi aprimorado para melhor experiência.

- **Ajustes no fluxo de quiz:**
  - Pontuação do usuário é salva automaticamente ao final do quiz, se estiver logado.
  - Mensagens de incentivo e feedback visual aprimorados.
  - **As alternativas de ano nas perguntas do quiz agora respeitam a década escolhida pelo usuário.**
  - Feedback de resposta (correta/incorreta) centralizado, colorido e sempre visível, sem ser cortado.
  - Título da pergunta com maior contraste.
  - Ajuste automático do tamanho da janela e fontes para evitar cortes de texto.

- **Tela inicial reorganizada:**
  - Botões padronizados em tamanho, espaçamento e alinhamento central.
  - Visual mais limpo e agradável.

---

## 📅 Histórico de Atualizações

- **[08/06/2025]**
  - Correção do filtro de alternativas do quiz por década.
  - Ajuste visual do feedback de resposta.
  - Exclusão do admin do ranking.
  - Melhoria na tela inicial e fluxo de login.
  - Ajuste de fontes e layout para melhor usabilidade.

- **[07/06/2025]**
  - Implementação do banco de jogadores e autenticação.
  - Novas telas: login, cadastro, administração de jogadores e ranking.
  - Integração do fluxo de login/admin/usuário comum.
  - Salvamento automático de pontuação.

---

**Para mais detalhes sobre cada modificação, consulte os comentários no código-fonte das respectivas telas e módulos.**

---

## 📈 Próximos Passos / Roadmap

* **Persistência de Configurações**: salvar configurações do usuário em JSON para recarregar na próxima sessão.