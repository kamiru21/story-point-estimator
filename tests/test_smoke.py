"""Smoke tests: make sure every app file is valid Python.

These compile the code without running it, so no network access,
API keys or Streamlit server are needed.
"""
import pathlib
import py_compile

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent
APP_FILES = sorted(
    p for p in ROOT.rglob("*.py")
    if ".git" not in p.parts and "tests" not in p.parts
)


def test_app_files_exist():
    assert (ROOT / "main.py").exists()


@pytest.mark.parametrize("path", APP_FILES, ids=lambda p: str(p.relative_to(ROOT)))
def test_compiles(path):
    py_compile.compile(str(path), doraise=True)
