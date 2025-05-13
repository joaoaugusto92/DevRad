import pandas as pd

def search_movies(keyword: str = None, genre: str = None, decade: str = None):
    """
    Retorna um DataFrame de filmes filtrados por palavra-chave opcional, gênero e década,
    ordenados de forma decrescente por bilheteria mundial.
    """
    df = pd.read_csv(
        "DataSet/world_imdb_movies_top_movies_per_year.csv",
        sep=",", encoding="utf-8"
    )
    results = df.copy()

    # Filtro por palavra-chave no título
    if keyword:
        kw = keyword.lower().split()
        results = results[
            results["title"].str.lower()
                .apply(lambda title: all(w in title for w in kw))
        ]

    # Filtro por gênero
    if genre:
        results = results[
            results['genre'].str.contains(genre, case=False, na=False)
        ]

    # Filtro por década
    if decade:
        start = int(decade)
        end = start + 9
        results['year'] = pd.to_numeric(results['year'], errors='coerce')
        results = results[
            (results['year'] >= start) &
            (results['year'] <= end)
        ]

    # Ordena por bilheteria global
    return results.sort_values(by="gross_world_wide", ascending=False)

def get_distinct_genres():
    """
    Retorna uma lista de todos os gêneros distintos presentes no banco de dados,
    considerando múltiplos gêneros separados por vírgulas.
    """
    df = pd.read_csv(
        "DataSet/world_imdb_movies_top_movies_per_year.csv",
        sep=",", encoding="utf-8"
    )
    genres = df['genre'].dropna().str.split(',').explode().str.strip().unique()
    genres = sorted(genres)
    return genres