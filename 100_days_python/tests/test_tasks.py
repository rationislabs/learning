import tasks


def make(root, day, *files):
    d = root / f"day_{day}" / "projects"
    d.mkdir(parents=True)
    for f in files:
        (d / f).write_text("")


def test_title():
    assert tasks.title("higher_or_lower_project") == "Higher or lower"
    assert tasks.title("band_name_generator") == "Band name generator"


def test_table_lists_days_in_order_and_skips_helpers(tmp_path):
    make(tmp_path, 2, "tip_calculator_project.py", "project.py")
    make(tmp_path, 10, "calculator_project.py", "art.py")
    make(tmp_path, 6, "Untitled Document")
    assert tasks.table(tmp_path).splitlines()[2:] == [
        "| 2 | Project, Tip calculator | [day_2](day_2/projects/) |",
        "| 6 | — | [day_6](day_6/projects/) |",
        "| 10 | Calculator | [day_10](day_10/projects/) |",
    ]


def test_new_day_creates_the_next_file_and_updates_both_readmes(tmp_path):
    make(tmp_path, 15, "coffee_machine_project.py")
    (tmp_path.parent / "README.md").write_text(
        "- 100 Days of Code: The Complete Python Pro Bootcamp (in progress, days 1–15)\n"
    )
    path = tasks.create_day(tmp_path, "Quiz game")
    assert path == tmp_path / "day_16" / "projects" / "quiz_game.py"
    assert path.read_text() == '"""Day 16: Quiz game"""\n'
    assert "| 16 | Quiz game | [day_16](day_16/projects/) |" in (tmp_path / "README.md").read_text()
    assert "(in progress, days 1–16)" in (tmp_path.parent / "README.md").read_text()
