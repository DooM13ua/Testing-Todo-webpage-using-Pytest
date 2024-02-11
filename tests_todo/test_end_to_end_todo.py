import time
import pytest
import re
from modules_todo.todo_modules import ToDo
from playwright.sync_api import Page, expect, sync_playwright


@pytest.fixture(scope="module")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        yield page
        browser.close()

def test_end_to_end_positive(page):
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")

    # 1.Add todos: a, b, c, d, e
    todo.add_task("a")
    todo.add_task("b")
    todo.add_task("c")
    todo.add_task("d")
    todo.add_task("e")
    time.sleep(2)
    # 2.Assert:
    assert todo.get_active_task() == ["a", "b", "c", "d", "e"]
    assert todo.get_items_left() == 5

    # 3.Update item "a" as "a-update"


