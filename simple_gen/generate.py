import os
import shutil
import subprocess
import time

import toml
from pathlib import Path
from typing import Optional
from simple_gen.utils import run_command


def generate_api(package_name: str, swagger_url: str, template: Optional[str] = None) -> None:
    command = [
        "java", "-jar", ".venv/bin/openapi-generator-cli-7.10.0.jar",
        "generate", "-i", swagger_url,
        "-g", "python",
        "-o", f"./{package_name}",
        "--library", "asyncio",
        "--package-name", package_name,
        "--skip-validate-spec"
    ]
    if template:
        command.extend(["-t", template])

    run_command(command)


def replace_imports_in_files(directory: str, package_name: str) -> None:
    from_search_pattern = f"from {package_name}"
    import_search_pattern = f"import {package_name}"
    replacement_pattern = f"clients.http.{package_name}"
    path = Path(directory)
    for file_path in path.rglob("*.py"):
        with file_path.open("r", encoding="utf-8") as file:
            lines = file.readlines()

        updated_lines = []
        for line in lines:
            line = line.replace(from_search_pattern, f"from {replacement_pattern}")
            line = line.replace(import_search_pattern, f"import {replacement_pattern}")
            line = line.replace(
                f"klass = getattr({package_name}.models, klass)",
                f"klass = getattr(clients.http.{package_name}.models, klass)",
            )
            updated_lines.append(line)

        with file_path.open("w", encoding="utf-8") as file:
            file.writelines(updated_lines)


def move_files(package_name: str) -> None:
    if os.path.exists(f"clients/http/{package_name}"):
        shutil.rmtree(f"clients/http/{package_name}")
    shutil.move(f"{package_name}/{package_name}", "clients/http")
    shutil.rmtree(f"{package_name}")


def generate(template: Optional[str] = None) -> None:
    with open("project.toml") as config_file:
        config = toml.load(config_file)

    for http_service in config["http"]:
        package_name = http_service["service_name"].replace("-", "_")
        swagger_url = http_service["swagger"]
        generate_api(package_name, swagger_url, template)
        move_files(package_name)
        replace_imports_in_files("clients/http", package_name)
