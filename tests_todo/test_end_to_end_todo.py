import pytest
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
    page.wait_for_timeout(3000)
    # 2.Assert
    assert todo.get_active_task() == ["a", "b", "c", "d", "e"]
    assert todo.get_tasks_left() == 5

    # 3.Update item "a" as "a-update"
    todo.edit_by_enter("a", "a-update")
    page.wait_for_timeout(3000)

    # 4.Assert
    assert todo.get_active_task() == ["a-update", "b", "c", "d", "e"]
    assert todo.get_tasks_left() == 5

    # 5.Check completed 'b' todos
    todo.check_task("b")
    page.wait_for_timeout(3000)

    # 6.Assert
    assert todo.get_tasks_left() == 4
    assert todo.get_completed_tasks() == ["b"]
    assert todo.get_active_task() == ["a-update", "c", "d", "e"]

    # 7.Check completed a-update, c
    todo.check_task("a-update")
    todo.check_task("c")
    page.wait_for_timeout(3000)

    # 8.Assert
    assert todo.get_completed_tasks() == ["a-update", "c", "b"]
    assert todo.get_active_task() == ["d", "e"]
    assert todo.get_tasks_left() == 2