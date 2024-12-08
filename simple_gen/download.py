import os
import platform
import shutil

import requests


def download() -> None:
    url = (
        "https://repo1.maven.org/maven2/org/openapitools/openapi-generator-cli/7.10.0/openapi-generator-cli-7.10.0.jar"
    )
    with requests.get(url, stream=True, timeout=100, verify=False) as response:  # noqa: S501
        response.raise_for_status()
        destination = "openapi-generator-cli-7.10.0.jar"
        with open(destination, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        if platform.system() != "Windows":
            # make it executable on *nix platforms equal to as of chmod 755
            os.chmod(destination, 0o755)  # noqa: S103
    shutil.move("openapi-generator-cli-7.10.0.jar", ".venv/bin/openapi-generator-cli-7.10.0.jar")


def init() -> None:
    if not os.path.exists(".venv/bin/openapi-generator-cli-7.10.0.jar"):
        download()
    print("Downloaded openapi-generator-cli-7.10.0.jar")
    with open("project.toml", "w") as f:
        ...
