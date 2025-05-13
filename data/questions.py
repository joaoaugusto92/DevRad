# data/questions.py
import pandas as pd
from services.moviesService import search_movies
import random

QUESTIONS = [
    {
        'question': 'Qual é o maior planeta do sistema solar?',
        'options': ['Terra', 'Júpiter', 'Marte', 'Saturno'],
        'answer': 1
    },
    {
        'question': 'Quantos lados tem um triângulo?',
        'options': ['3', '4', '5', '6'],
        'answer': 0
    },
    {
        'question': 'Qual é a capital do Brasil?',
        'options': ['Rio de Janeiro', 'São Paulo', 'Brasília', 'Salvador'],
        'answer': 2
    },
    {
        'question': 'Qual é o resultado de 2 + 2?',
        'options': ['3', '4', '5', '6'],
        'answer': 1
    },
    {
        'question': 'Qual é o animal conhecido como "Rei da Selva"?',
        'options': ['Elefante', 'Tigre', 'Leão', 'Gorila'],
        'answer': 2
    },
    {
        'question': 'Qual é a cor do céu em um dia claro?',
        'options': ['Verde', 'Azul', 'Amarelo', 'Vermelho'],
        'answer': 1
    },
]

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
    
    for _, row in topN.iterrows():
        correct_year = row['year']
        wrong_years = pd.Series([correct_year + i for i in range(-3, 4) if i != 0]).sample(3).tolist()
        options = [correct_year] + wrong_years
        random.shuffle(options)
        QUESTIONS.append({
            'question': f'Em que ano o filme "{row["title"]}" foi lançado?',
            'options': [str(year) for year in options],
            'answer': options.index(correct_year)
        })

    return QUESTIONS