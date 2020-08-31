from . import cli as _cli, click
from biograf_seeder.database.module import movie
from biograf_seeder.database.errors import DbQueryError
from biograf_seeder.core.output import Table


@_cli.command(name="lista")
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
