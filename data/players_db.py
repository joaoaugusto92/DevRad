import sqlite3

DB_PATH = "data/players.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_players():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome, email FROM players")
    players = c.fetchall()
    conn.close()
    return players

def add_player(nome, email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO players (nome, email) VALUES (?, ?)", (nome, email))
    conn.commit()
    conn.close()

def update_player(player_id, nome, email):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("UPDATE players SET nome=?, email=? WHERE id=?", (nome, email, player_id))
    conn.commit()
    conn.close()

def search_players_by_id(player_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome, email FROM players WHERE id=?", (player_id,))
    players = c.fetchall()
    conn.close()
    return players

def search_players_by_name(nome):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, nome, email FROM players WHERE nome LIKE ?", (f"%{nome}%",))
    players = c.fetchall()
    conn.close()
    return players

def delete_player(player_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE id=?", (player_id,))
    conn.commit()
    conn.close()