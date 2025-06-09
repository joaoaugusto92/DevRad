# data/questions.py

import pandas as pd
from services.moviesService import search_movies
import random

QUESTIONS = []

def get_questions(genre: str = None, decade: str = None, top_n: int = 15):
    """
    Busca os filmes top_n por bilheteria usando os filtros de gênero e década,
    e imprime título, ano, gênero e bilheteria formatada no console.
    """
    df = search_movies(keyword=None, genre=genre, decade=decade)
    topN = df.head(top_n)

    def fmt(amount):
        if pd.isnull(amount): return "N/A"
        a = float(amount)
        if a >= 1e9: return f"{a/1e9:.1f}B"
        if a >= 1e6: return f"{a/1e6:.1f}M"
        if a >= 1e3: return f"{a/1e3:.1f}K"
        return f"{a:.0f}"

    topN = topN.sample(n=min(5, len(topN)))

    QUESTIONS.clear()  # Limpa perguntas antigas

    # Descobre o intervalo da década
    if decade is not None:
        decade_start = int(decade)
        decade_end = decade_start + 9
    else:
        decade_start = df['year'].min()
        decade_end = df['year'].max()

    for _, row in topN.iterrows():
        correct_year = row['year']
        # Gera alternativas só com anos da década escolhida
        anos_decada = df[(df['year'] >= decade_start) & (df['year'] <= decade_end)]['year'].unique().tolist()
        # Remove o ano correto para não duplicar
        anos_decada = [ano for ano in anos_decada if ano != correct_year]
        # Seleciona até 3 anos errados
        wrong_years = random.sample(anos_decada, min(3, len(anos_decada)))
        options = [correct_year] + wrong_years
        random.shuffle(options)
        QUESTIONS.append({
            'question': f'Em que ano o filme "{row["title"]}" foi lançado?',
            'options': [str(year) for year in options],
            'answer': options.index(correct_year)
        })

    return QUESTIONS