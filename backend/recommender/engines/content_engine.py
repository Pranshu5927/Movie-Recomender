import pandas as pd

from sqlalchemy import create_engine

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)

from nltk.stem.porter import PorterStemmer

from db.database import DATABASE_URL


# ---------------------------------
# LOAD DATABASE
# ---------------------------------
engine = create_engine(DATABASE_URL)


# ---------------------------------
# STEMMING
# ---------------------------------
ps = PorterStemmer()


def stem(text):

    words = []

    for word in text.split():

        words.append(
            ps.stem(word)
        )

    return " ".join(words)


# ---------------------------------
# LOAD + PROCESS DATASETS
# ---------------------------------
try:
    movies_df = pd.read_sql(
        "SELECT * FROM movies",
        engine
    )

    tags_df = pd.read_sql(
        "SELECT * FROM tags",
        engine
    )

    if movies_df.empty:
        raise ValueError("movies table is empty")

    # ---------------------------------
    # CLEAN GENRES
    # ---------------------------------
    movies_df["genres_clean"] = (
        movies_df["genres"]
        .str.replace("|", " ", regex=False)
    )

    movies_df["genres_clean"] = (
        movies_df["genres_clean"]
        .str.replace(
            "(no genres listed)",
            "",
            regex=False
        )
    )

    # ---------------------------------
    # AGGREGATE TAGS
    # ---------------------------------
    movie_tags = (
        tags_df
        .groupby("movie_id")["tag"]
        .apply(
            lambda x: " ".join(
                x.astype(str)
            )
        )
        .reset_index()
    )

    # ---------------------------------
    # MERGE MOVIES + TAGS
    # ---------------------------------
    movies_df = movies_df.merge(
        movie_tags,
        on="movie_id",
        how="left"
    )

    # ---------------------------------
    # HANDLE NULL TAGS
    # ---------------------------------
    movies_df["tag"] = (
        movies_df["tag"]
        .fillna("")
    )

    # ---------------------------------
    # CREATE CONTENT COLUMN
    # ---------------------------------
    movies_df["content"] = (
        movies_df["genres_clean"] + " " +
        movies_df["tag"]
    )

    # ---------------------------------
    # LOWERCASE
    # ---------------------------------
    movies_df["content"] = (
        movies_df["content"]
        .str.lower()
    )

    # ---------------------------------
    # STEMMING
    # ---------------------------------
    movies_df["content"] = (
        movies_df["content"]
        .apply(stem)
    )

    # ---------------------------------
    # TF-IDF VECTORIZATION
    # ---------------------------------
    vectorizer = TfidfVectorizer(
        max_features=5000,
        stop_words="english"
    )

    vectors = vectorizer.fit_transform(
        movies_df["content"]
    ).toarray()

    # ---------------------------------
    # COSINE SIMILARITY
    # ---------------------------------
    similarity = cosine_similarity(
        vectors
    )

    print(
        "Content engine loaded successfully!"
    )

except Exception as e:
    print(f"Warning: Could not load content engine data at startup: {e}")
    print("Content-based recommendations will be unavailable until data is seeded and the backend is restarted.")
    movies_df = None
    tags_df = None
    vectorizer = None
    vectors = None
    similarity = None
