from typing import Optional

import click

from simple_gen.download import init
from simple_gen.generate import generate
from simple_gen.utils import setup


@click.group()
def cli() -> None: ...


@click.command("setup")
@click.option("--template", "-t", required=False)
def setup_command(template: Optional[str]) -> None:
    setup(template=template)
    init()


@click.command("init")
def init_command() -> None:
    init()


@click.command("generate")
def generate_command() -> None:
    generate()


cli.add_command(setup_command)
cli.add_command(init_command)
cli.add_command(generate_command)

if __name__ == "__main__":
    cli()
