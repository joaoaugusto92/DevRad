import sqlite3

DB_PATH = "data/players.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL,
            senha TEXT NOT NULL,
            pontuacao INTEGER DEFAULT 0,
            is_admin INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()

def add_player(nome, email, senha, is_admin=0):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO players (nome, email, senha, is_admin) VALUES (?, ?, ?, ?)", (nome, email, senha, is_admin))
    conn.commit()
    conn.close()

def authenticate_player(email, senha):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome, is_admin FROM players WHERE email=? AND senha=?", (email, senha))
    user = c.fetchone()
    conn.close()
    return user  # None se não achou

def update_score(player_id, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE players SET pontuacao=? WHERE id=?", (score, player_id))
    conn.commit()
    conn.close()

def get_player_score(player_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT pontuacao FROM players WHERE id=?", (player_id,))
    score = c.fetchone()
    conn.close()
    return score[0] if score else 0

def get_ranking():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    # Só pega usuários que NÃO são admin
    c.execute("SELECT nome, pontuacao FROM players ORDER BY pontuacao DESC LIMIT 10")
    ranking = c.fetchall()
    conn.close()
    return ranking

def get_players():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome, email FROM players")
    players = c.fetchall()
    conn.close()
    return players

def update_player(player_id, nome, email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE players SET nome=?, email=? WHERE id=?", (nome, email, player_id))
    conn.commit()
    conn.close()

def delete_player(player_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE id=?", (player_id,))
    conn.commit()
    conn.close()

def search_players_by_id(player_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome, email FROM players WHERE id=?", (player_id,))
    result = c.fetchall()
    conn.close()
    return result

def search_players_by_name(name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome, email FROM players WHERE nome LIKE ?", ('%' + name + '%',))
    result = c.fetchall()
    conn.close()
    return result

def exists_admin():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT 1 FROM players WHERE is_admin=1 LIMIT 1")
    exists = c.fetchone() is not None
    conn.close()
    return exists