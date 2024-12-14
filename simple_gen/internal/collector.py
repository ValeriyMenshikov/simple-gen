from pathlib import Path


class ClientCollector:
    base_path: Path = Path(".") / "clients" / "http"

    def collect_clients(self) -> list[dict[str, str]]:
        clients = []
        for file_path in self.base_path.rglob("*.py"):
            if str(file_path.parent).endswith("api") and file_path.name.endswith("__init__.py"):
                with file_path.open("r", encoding="utf-8") as file:
                    lines = file.readlines()

                for line in lines:
                    if line.startswith("from"):
                        client = {
                            "import": line.strip(),
                            "client": line.split()[-1],
                            "package": str(file_path.parent.parent).split("/")[-1],
                        }
                        clients.append(client)

        return clients
