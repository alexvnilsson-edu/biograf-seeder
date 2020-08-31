from typing import List
from biograf_seeder.database import (
    make_cursor,
    commit,
    MySQLCursor,
    DbQueryError,
    NotFoundError,
)

from biograf_seeder.database.types import Genre


def find(
    name: str, cursor: MySQLCursor = None, create_if_not_exist: bool = False
) -> int:
    if cursor is None:
        cursor = make_cursor()
        cursor_close = True
    else:
        cursor_close = False

    film_genre_id = None

    try:
        result_args = cursor.callproc("FindMovieGenre", [name, 0])

        film_genre_id = result_args[1]
    except Exception:
        raise

    if film_genre_id is None and create_if_not_exist == True:
        # Skapa ny genre om den inte finns.
        film_genre_id = create(name, name, cursor)

    if cursor_close == True:
        commit()
        cursor.close()

    return film_genre_id


def create(name: str, description: str = "", cursor: MySQLCursor = None):
    if cursor is None:
        cursor = make_cursor()
        cursor_close = True
    else:
        cursor_close = False

    genre_id = None

    result = cursor.callproc("InsertMovieGenre", [name, description, 0])

    genre_id = result[2]

    if genre_id is None:
        raise Exception("genre_id är None.")

    if cursor_close == True:
        commit()
        cursor.close()

    return genre_id


def list(limit: int = 25, cursor: MySQLCursor = None) -> List:
    if cursor is None:
        cursor = make_cursor()
        cursor_close = True
    else:
        cursor_close = False

    genre = []

    query = "SELECT ID, Namn, Beskrivning FROM FilmGenre LIMIT %s"

    cursor.execute(query, (limit,))

    for (ID, Namn, Beskrivning) in cursor:
        genre.append({"ID": ID, "Namn": Namn, "Beskrivning": Beskrivning})

    if cursor_close == True:
        commit()
        cursor.close()

    return genre
