import os
import re
from pathlib import Path, PurePosixPath

from core.exceptions import PathException


def normalize_unix_path(unix_path: str) -> Path:
    cleaned_path = unix_path.strip("/")
    cleaned_path = re.sub(r"/+", "/", cleaned_path)

    if not cleaned_path:
        return Path(".")

    posix_path = PurePosixPath(cleaned_path)

    for part in posix_path.parts:
        if part in ("..", ".") or part.startswith("."):
            raise PathException(
                path=unix_path, reason=f"Небезпечний елемент шляху: {part}"
            )

        if os.name == "nt":
            forbidden_chars = '<>:"|?*'
            if any(char in part for char in forbidden_chars):
                raise PathException(
                    path=unix_path, reason=f"Заборонені символи у назві: {part}"
                )

            forbidden_names = {
                "CON",
                "PRN",
                "AUX",
                "NUL",
                "COM1",
                "COM2",
                "COM3",
                "COM4",
                "COM5",
                "COM6",
                "COM7",
                "COM8",
                "COM9",
                "LPT1",
                "LPT2",
                "LPT3",
                "LPT4",
                "LPT5",
                "LPT6",
                "LPT7",
                "LPT8",
                "LPT9",
            }
            if part.upper() in forbidden_names:
                raise PathException(
                    path=unix_path, reason=f"Заборонена назва файлу для Windows: {part}"
                )

    return Path(*posix_path.parts)


def create_safe_file_path(base_path: Path, relative_path: str, filename: str) -> Path:
    normalized_path = normalize_unix_path(relative_path)

    full_dir_path = base_path / normalized_path
    full_file_path = full_dir_path / filename

    try:
        full_file_path.resolve().relative_to(base_path.resolve())
    except ValueError:
        raise PathException(
            path=relative_path, reason="Шлях виходить за межі дозволеної директорії"
        )

    return full_file_path
