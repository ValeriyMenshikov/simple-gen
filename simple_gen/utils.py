import platform
import shutil
import subprocess
import sys
from pathlib import Path
from typing import List, Optional

import colorama
from colorama import Fore
from cookiecutter.main import cookiecutter


def run_command(command: List[str], ignore_error: bool = False) -> str:
    result = subprocess.run(args=command, text=True, capture_output=True)
    print(result.stdout)
    if result.returncode != 0 and not ignore_error:
        print(f"{Fore.RED}Error: {result.stderr}, for command: {' '.join(command)}")
        sys.exit(1)
    return result.stdout.strip()


def check_git_repository() -> None:
    is_work_tree = run_command(["git", "rev-parse", "--is-inside-work-tree"], ignore_error=True)
    if not is_work_tree:
        print(
            f"{Fore.RED}It looks like you are using the script in a location other than your local repository. "
            f"Clone the created repository and call this script from the repository directory."
        )
        sys.exit(1)


def get_git_user_info() -> tuple:
    user_email = run_command(["git", "config", "--get", "user.email"], ignore_error=True)
    user_name = run_command(["git", "config", "--get", "user.name"], ignore_error=True)
    authors = f"{user_name or 'user_name'} <{user_email or 'user_name@ozon.ru'}>"
    return user_email, authors


def get_repository_info() -> str:
    print(f"{Fore.BLUE}Repository:")
    remote = run_command(["git", "config", "--get", "remote.origin.url"])
    return remote.split("/")[-1].split(".git")[0]


def create_project(template: str) -> None:
    print(f"{Fore.BLUE}Create project...")
    parent_dir = str(Path.cwd())
    service_name = Path.cwd().name
    repository = get_repository_info()
    user_email, authors = get_git_user_info()
    context = {
        "user_email": user_email,
        "authors": authors,
        "project_slug": service_name,
        "repository": repository,
    }
    cookiecutter(
        template,
        no_input=True,
        overwrite_if_exists=True,
        output_dir=parent_dir,
        extra_context=context,
    )
    print(f"{Fore.GREEN}Project initialized successfully!")


def install_dependencies(python_version: str) -> None:
    print(f"{Fore.BLUE}Install dependencies...")
    run_command([f"{python_version}", "-m", "poetry", "install", "--no-root"])


def nuke_initialization(python_version: str) -> None:
    print(f"{Fore.BLUE}Run nuke init...")
    run_command([f"{python_version}", "-m", "poetry", "run", "nuke", "init"])


def copy_k8s_values() -> None:
    shutil.copyfile(".o3/k8s/values_local.example.yaml", ".o3/k8s/values_local.yaml")


def setup(template: Optional[str] = None) -> None:
    colorama.init(autoreset=True)
    template = template or "https://github.com/ValeriyMenshikov/project-template"
    check_git_repository()
    create_project(template)

