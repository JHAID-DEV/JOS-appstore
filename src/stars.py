#!/usr/bin/env python3

import os
import shutil
import subprocess
from pathlib import Path

from .utils import DATA_DIR, PROJECT_ROOT, file_autoreload

STARS_DIR = DATA_DIR / "stars"


class AppstoreStars:
    def __init__(self) -> None:
        self.stars: dict[str, set[int]] = {}
        STARS_DIR.mkdir(exist_ok=True)

    def add(self, app: str, user: int) -> None:
        self.stars.get(app, set()).add(user)
        self.save(app)

    def remove(self, app: str, user: int) -> None:
        self.stars.get(app, set()).remove(user)
        self.save(app)

    def save(self, app: str) -> None:
        app_file = STARS_DIR / app
        app_file.write_text("\n".join(str(user) for user in self.stars[app]))

    def save_all(self) -> None:
        for app in self.stars.keys():
            self.save(app)

    def read(self) -> None:
        for file in STARS_DIR.iterdir():
            if file.name.startswith("."):
                continue
            self.stars[file.name] = set(
                int(line.strip()) for line in file.read_text().strip().splitlines()
            )

    def read_legacy(self) -> None:
        legacy_stars_dir = PROJECT_ROOT / ".stars"
        if not legacy_stars_dir.exists():
            return

        stars = {}
        for folder, _, files in os.walk(legacy_stars_dir):
            app_id = folder.split("/")[-1]
            if not app_id:
                continue
            stars[app_id] = set(files)

        self.stars = stars

        self.save_all()
        shutil.rmtree(legacy_stars_dir)
