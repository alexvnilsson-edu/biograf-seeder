from . import click, cli
from database.module import genre
from database.errors import DbQueryError


@cli.command(name="ny", no_args_is_help=True)
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
