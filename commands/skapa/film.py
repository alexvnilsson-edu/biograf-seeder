from . import click, cli
from database.module import movie
from database.errors import DbQueryError


@cli.command(name="film")
@click.option("--titel", required=True, help="Filmens titel.")
@click.option("--genre", multiple=True, help="Genre som filmen tillhör.")
@click.option(
    "--produktion", required=False, help="Året då filmen producerades (4 siffror)."
)
@click.option("--utgivning", required=True, help="Året då filmen utgavs (4 siffror).")
def cli(titel, genre, produktion, utgivning):
    genrer = ", ".join(genre)
    click.echo(f"skapa film '{titel}', genre(r): '{genrer}'")

    try:
        movie_id = movie.create(titel, produktion, utgivning)
    except DbQueryError as e:
        print(f"Kunde inte skapa filmen '{titel}' ({e}).")

    for g in genre:
        movie.relate_genre(movie_id, g)
