from . import click, cli
from database.module import movie
from database.errors import DbQueryError
from core.output import Table


@cli.command(name="lista")
def cli():
    movies = movie.list()
    table_header = ["ID", "Titel", "OrginalTitel", "ProduktionÅr", "UtgivningÅr"]
    table_rows = []

    t = Table()
    t.set_header("ID", "Titel", "OrginalTitel", "ProduktionÅr", "UtgivningÅr")

    for m in movies:
        t.append(m)

    print(t.rows)

    t.print()
