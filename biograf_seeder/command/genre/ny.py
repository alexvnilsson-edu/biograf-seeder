from . import click, cli as group
from biograf_seeder.database.module import genre
from biograf_seeder.database.errors import DbQueryError


@group.command(name="ny", no_args_is_help=True)
@click.option("--namn", required=True, help="Beteckningen av genren.")
@click.option("--beskrivning", required=False, help="Beskrivning av genren.")
def cli(namn, beskrivning):
    try:
        genre_id = genre.create(namn, beskrivning)
        click.echo(
            f"Skapade genre [ ID = {genre_id}, Namn = {namn}, Beskrivning = {beskrivning} ]."
        )
    except Exception as e:
        click.echo(f"Kunde inte skapa genre '{namn}' ({e}).")
