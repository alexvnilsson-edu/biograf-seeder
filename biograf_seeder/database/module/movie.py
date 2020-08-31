from typing import List
from .. import make_cursor, commit, MySQLCursor
from ..errors import NotFoundError, DbQueryError
from ..types import Movie


def create(
    title: str, production_year: int, release_year: int, cursor: MySQLCursor = None
) -> int:
    if cursor is None:
        cursor = make_cursor()
        cursor_close = True
    else:
        cursor_close = False

    movie_id = None

    try:
        result = cursor.callproc(
            "InsertMovie", [title, production_year, release_year, 0]
        )
        movie_id = result[3]
    except Exception as e:
        raise

    if movie_id is None:
        raise Exception("movie_id är None.")

    if cursor_close == True:
        commit()
        cursor.close()

    return movie_id


def relate_genre(movie_id: int, genre: str, cursor: MySQLCursor = None) -> int:
    if cursor is None:
        cursor = make_cursor()
        cursor_close = True
    else:
        cursor_close = False

    movie_genre_id = None

    try:
        result = cursor.callproc("InsertMovieGenreRelation", [movie_id, genre, 0])
        movie_genre_id = result[2]
    except Exception as e:
        raise

    if cursor_close == True:
        commit()
        cursor.close()

    return movie_genre_id


def list(limit: int = 25, cursor: MySQLCursor = None) -> List:
    if cursor is None:
        cursor = make_cursor()
        cursor_close = True
    else:
        cursor_close = False

    genre = []

    query = "SELECT ID, Titel, OrginalTitel, ProduktionÅr, UtgivningÅr FROM FilmTitel LIMIT %s"

    cursor.execute(query, (limit,))

    for (ID, Titel, OrginalTitel, ProduktionÅr, UtgivningÅr) in cursor:
        genre.append(
            {
                "ID": ID,
                "Titel": Titel,
                "OrginalTitel": OrginalTitel,
                "ProduktionÅr": ProduktionÅr,
                "UtgivningÅr": UtgivningÅr,
            }
        )

    if cursor_close == True:
        commit()
        cursor.close()

    return genre
