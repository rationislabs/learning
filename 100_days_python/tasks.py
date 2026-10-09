"""Developer tasks. List them with `uv run inv --list`."""

from __future__ import annotations

import re
from pathlib import Path

from invoke import task

ROOT = Path(__file__).parent
HELPERS = {"art", "game_data"}  # course helper files, not projects
HEADER = "| Day | Projects | Folder |\n|---|---|---|\n"
INTRO = """# 100 Days of Code

My daily projects from the Udemy course "100 Days of Code: The Complete Python Pro
Bootcamp". Only my own code is here; the course's starter files and assets stay with the
course.

Start a new day with `uv run inv new-day "project name"`; the table below is rebuilt from the
folders.

"""


def title(stem: str) -> str:
    words = stem.removesuffix("_project").replace("_", " ").replace(".", " ").strip()
    return words[:1].upper() + words[1:]


def _days(root: Path) -> list[int]:
    return sorted(
        int(m.group(1)) for p in root.iterdir() if (m := re.fullmatch(r"day_(\d+)", p.name))
    )


def table(root: Path) -> str:
    rows = []
    for n in _days(root):
        stems = sorted(p.stem for p in (root / f"day_{n}" / "projects").glob("*.py"))
        names = ", ".join(title(s) for s in stems if s not in HELPERS) or "—"
        rows.append(f"| {n} | {names} | [day_{n}](day_{n}/projects/) |")
    return HEADER + "\n".join(rows) + "\n"


def create_day(root: Path, topic: str) -> Path:
    """The next day's project file; rebuilds this README and bumps the course line one level up."""
    n = max(_days(root), default=0) + 1
    path = (
        root
        / f"day_{n}"
        / "projects"
        / f"{re.sub(r'\W+', '_', topic.strip().lower()).strip('_')}.py"
    )
    path.parent.mkdir(parents=True)
    path.write_text(f'"""Day {n}: {topic.strip()}"""\n')
    (root / "README.md").write_text(INTRO + table(root))
    top = root.parent / "README.md"
    if top.exists():
        top.write_text(
            re.sub(r"\(in progress, days 1–\d+\)", f"(in progress, days 1–{n})", top.read_text())
        )
    return path


@task(name="new-day")
def new_day(c, topic):
    """Create the next day's project file: uv run inv new-day "quiz game"."""
    print(f"created {create_day(ROOT, topic).relative_to(ROOT)}")


@task
def index(c):
    """Rebuild the README table from the day folders."""
    (ROOT / "README.md").write_text(INTRO + table(ROOT))


@task
def lint(c):
    c.run("uv run ruff check . && uv run ruff format --check .")
