from pathlib import Path

from simple_gen.internal.collector import ClientCollector
from inflection import underscore, camelize
from jinja2 import Environment, FileSystemLoader


class Generator:

    def __init__(self) -> None:
        self.client_collector = ClientCollector()
        self.templates_dir = Path(__file__).parent.parent / "templates" / "tests"
        self.env = Environment(loader=FileSystemLoader(self.templates_dir), autoescape=True)  # type: ignore
        self.env.filters["to_snake_case"] = underscore
        self.env.filters["to_camel_case"] = camelize

    def generate(self) -> str:
        fixture_template = self.env.get_template("conftest.jinja2")
        fixtures = fixture_template.render(
            clients=self.client_collector.collect_clients()
        )
        with open("conftest.py", "w") as f:
            f.write(fixtures)

        return fixtures
