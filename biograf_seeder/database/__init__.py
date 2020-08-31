import sys
import mysql.connector
from mysql.connector import Error
from mysql.connector.cursor_cext import CMySQLCursor as MySQLCursor
from biograf_seeder.core import config
from biograf_seeder.database.errors import (
    DbConnectionError,
    DbQueryError,
    NotFoundError,
)


def __connect(*args, **kwargs):
    connection = None
    connection_error = None
    try:
        connection = mysql.connector.connect(*args, **kwargs)
    except Error:
        raise DbConnectionError(connection_error)

    return connection


__connection = __connect(
    user=config.get("DATABASE_USER"),
    password=config.get("DATABASE_PASSWORD"),
    host=config.get("DATABASE_HOST"),
    database=config.get("DATABASE_DATABASE"),
)


def make_cursor() -> MySQLCursor:
    return __connection.cursor()


def commit():
    if __connection is None:
        raise Exception("Inte ansluten till MySQL.")

    __connection.commit()
