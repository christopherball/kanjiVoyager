#!/usr/bin/env python3

from __future__ import annotations

import shutil
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
DIST_DIR = REPO_ROOT / "dist"

FILE_MAP = {
    REPO_ROOT / "index.html": DIST_DIR / "index.html",
    REPO_ROOT / "css" / "index.css": DIST_DIR / "css" / "index.css",
    REPO_ROOT / "scripts" / "index.js": DIST_DIR / "scripts" / "index.js",
    REPO_ROOT / "data" / "kanjiData.json": DIST_DIR / "data" / "kanjiData.json",
}

ASSET_INCLUDE_EXTENSIONS = {".svg", ".png"}
ASSET_EXCLUDE_NAMES = {".DS_Store"}


def copy_file(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def copy_assets() -> int:
    asset_count = 0
    assets_root = REPO_ROOT / "assets"

    for source in assets_root.rglob("*"):
        if not source.is_file():
            continue
        if source.name in ASSET_EXCLUDE_NAMES:
            continue
        if source.suffix.lower() not in ASSET_INCLUDE_EXTENSIONS:
            continue

        destination = DIST_DIR / source.relative_to(REPO_ROOT)
        copy_file(source, destination)
        asset_count += 1

    return asset_count


def build_dist() -> None:
    if DIST_DIR.exists():
        shutil.rmtree(DIST_DIR)
    DIST_DIR.mkdir(parents=True, exist_ok=True)

    copied_files = 0
    for source, destination in FILE_MAP.items():
        copy_file(source, destination)
        copied_files += 1

    copied_files += copy_assets()

    print(f"Built dist bundle at {DIST_DIR}")
    print(f"Copied {copied_files} files")


if __name__ == "__main__":
    build_dist()
