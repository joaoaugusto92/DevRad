# data/questions.py

import pandas as pd
from services.moviesService import search_movies
import random

QUESTIONS = []

def fmt(amount):
    if pd.isnull(amount): return "N/A"
    a = float(amount)
    if a >= 1e9: return f"{a/1e9:.1f}B"
    if a >= 1e6: return f"{a/1e6:.1f}M"
    if a >= 1e3: return f"{a/1e3:.1f}K"
    return f"{a:.0f}"

def generate_question(row):
    question_types = ['year', 'oscars', 'nominations', 'gross', 'country', 'star']
    question_type = random.choice(question_types)
    if question_type == 'year':
        correct = row['year']
        if pd.isnull(correct):
            return None
        decade_start = (int(correct) // 10) * 10
        decade_years = [y for y in range(decade_start, decade_start + 10) if y != int(correct)]
        if len(decade_years) < 3:
            wrong = random.sample(decade_years, len(decade_years))
        else:
            wrong = random.sample(decade_years, 3)
        options = [int(correct)] + wrong
        random.shuffle(options)
        return {
            'question': f'Em que ano o filme "{row["title"]}" foi lançado?',
            'options': [str(opt) for opt in options],
            'answer': options.index(int(correct))
        }

    elif question_type == 'oscars':
        correct = int(row['oscar']) if pd.notnull(row['oscar']) else 0
        wrong = random.sample(range(max(0, correct - 3), correct + 4), 4)
        if correct not in wrong:
            wrong[random.randint(0, 3)] = correct
        random.shuffle(wrong)
        return {
            'question': f'Quantos Oscars o filme "{row["title"]}" ganhou?',
            'options': [str(opt) for opt in wrong],
            'answer': wrong.index(correct)
        }

    elif question_type == 'nominations':
        correct = int(row['nomination']) if pd.notnull(row['nomination']) else 0
        wrong = random.sample(range(max(0, correct - 3), correct + 4), 4)
        if correct not in wrong:
            wrong[random.randint(0, 3)] = correct
        random.shuffle(wrong)
        return {
            'question': f'Para quantos Oscars o filme "{row["title"]}" foi nomeado?',
            'options': [str(opt) for opt in wrong],
            'answer': wrong.index(correct)
        }

    elif question_type == 'gross':
        correct = row['gross_world_wide']
        correct_fmt = fmt(correct)
        wrong_values = [correct * factor for factor in [0.5, 1.5, 2.0]]
        wrong_fmt = [fmt(v) for v in wrong_values]
        options = [correct_fmt] + wrong_fmt
        random.shuffle(options)
        return {
            'question': f'Qual foi a bilheteria mundial do filme "{row["title"]}"?',
            'options': options,
            'answer': options.index(correct_fmt)
        }

    elif question_type == 'country':
        correct = row['country_origin']
        wrong = ['United States', 'United Kingdom', 'France', 'Germany', 'Japan', 'Brazil', 'Italy', 'Spain', 'India', 'South Korea', 'China']
        wrong = [c for c in wrong if c != correct]
        options = random.sample(wrong, 3) + [correct]
        random.shuffle(options)
        return {
            'question': f'Qual é o país de origem do filme "{row["title"]}"?',
            'options': options,
            'answer': options.index(correct)
        }

    elif question_type == 'star':
        # Pega lista de atores reais
        if pd.isnull(row['star']) or not isinstance(row['star'], str):
            return None  # Ignora caso não tenha dados válidos

        real_stars = [s.strip() for s in row['star'].split(',') if s.strip()]
        if not real_stars:
            return None

        correct = random.choice(real_stars)

        # Lista de atores genéricos para criar alternativas falsas
        fake_stars_pool = [
            'Tom Cruise', 'Scarlett Johansson', 'Brad Pitt',
            'Jennifer Lawrence', 'Chris Hemsworth', 'Emma Watson',
            'Ryan Gosling', 'Anne Hathaway', 'Christian Bale',
            'Meryl Streep', 'Robert Downey Jr.', 'Natalie Portman',
            'Leonardo DiCaprio', 'Kate Winslet', 'Hugh Jackman',
            'Julia Roberts', 'Denzel Washington', 'Sandra Bullock',
            'Will Smith', 'Angelina Jolie', 'Johnny Depp',
            'Tom Hanks', 'Morgan Freeman', 'Harrison Ford',
            'Al Pacino', 'Robert De Niro', 'Jack Nicholson',
        ]

        # Remove atores que estão no filme da lista de falsos
        fake_options = [name for name in fake_stars_pool if name not in real_stars]
        wrong = random.sample(fake_options, 3)

        options = wrong + [correct]
        random.shuffle(options)

        return {
            'question': f'Qual desses atores participou do filme "{row["title"]}"?',
            'options': options,
            'answer': options.index(correct)
        }


def get_questions(genre: str = None, decade: str = None, top_n: int = 15):
    QUESTIONS.clear()
    df = search_movies(keyword=None, genre=genre, decade=decade)
    topN = df.head(top_n)
    selected = topN.sample(n=min(5, len(topN)))

    for _, row in selected.iterrows():
        question = generate_question(row)
        if question:
            QUESTIONS.append(question)

    return QUESTIONS
