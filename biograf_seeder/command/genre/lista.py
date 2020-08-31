from . import click, cli as group
from biograf_seeder.database.module import genre
from biograf_seeder.database.errors import DbQueryError
from biograf_seeder.core.output import Table


@group.command(name="lista")
def cli():
    genres = genre.list()
    table_header = ["ID", "Namn", "Beskrivning"]
    table_rows = []

    t = Table()
    t.set_header("ID", "Namn", "Beskrivning")

    for g in genres:
        t.append(g)

    t.print()
