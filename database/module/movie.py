from .. import make_cursor, commit, MySQLCursor
from ..errors import NotFoundError, DbQueryError


def create(
    title: str, production_year: int, release_year: int, cursor: MySQLCursor = None
) -> int:
    if cursor is None:
        cursor = make_cursor()
        cursor_close = True
    else:
        cursor_close = False

    movie_id = None

    cursor.callproc("InsertMovie", [title, production_year, release_year, 0])
    movie_id = cursor.lastrowid

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


def find_genre(
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
    except Exception as e:
        raise

    if film_genre_id is None and create_if_not_exist == True:
        # Skapa ny genre om den inte finns.
        film_genre_id = create_genre(name, name, cursor)

    if cursor_close == True:
        commit()
        cursor.close()

    return film_genre_id


def create_genre(name: str, description: str = "", cursor: MySQLCursor = None):
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
