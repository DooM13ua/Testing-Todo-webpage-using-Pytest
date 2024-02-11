import time
import pytest
from playwright.sync_api import Page, expect, sync_playwright
from modules_todo.todo_modules import ToDo


@pytest.fixture(scope="function")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()


def test_logo_check(page):
    """Check header."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")

    assert page.locator("h1").text_content() == "todos"


def test_todo_field(page):
    """Check whether there is an input field."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")

    assert page.locator("input.new-todo").is_visible()


def test_todo_text(page):
    """Check if there is right text in active field 'What needs to be done?'."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")

    assert page.locator("input.new-todo").get_attribute("placeholder") == "What needs to be done?"


def test_add(page):
    """Test add new task."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.add_task("Task 2")
    todo.add_task("Task 3")

    assert todo.get_active_task() == ["Task 1", "Task 2", "Task 3"]


def test_complete_one(page):
    """Test complete button for one task."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.check_task("Task 1")

    completed_tasks = todo.get_completed_tasks()
    assert "Task 1" in completed_tasks


def test_complete_all(page):
    """Check if all completed tasks are displayed correctly."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.add_task("Task 2")
    todo.add_task("Task 3")
    todo.check_all_completed()

    assert todo.get_tasks_left() == 0
    assert todo.get_completed_tasks() == ["Task 1", "Task 2", "Task 3"]
    assert todo.get_active_task() == []


def test_activate_one(page):
    """Try to activate one task from completed."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.add_task("Task 2")
    todo.add_task("Task 3")
    todo.check_all_completed()
    todo.uncheck_task("Task 2")

    assert todo.get_tasks_left() == 1
    assert todo.get_completed_tasks() == ["Task 1", "Task 3"]
    assert todo.get_active_task() == ["Task 2"]


def test_activate_all(page):
    """Activate all completed tasks."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.add_task("Task 2")
    todo.add_task("Task 3")
    todo.check_all_completed()
    todo.uncheck_all_completed()

    assert todo.get_tasks_left() == 3
    assert todo.get_completed_tasks() == []
    assert todo.get_active_task() == ["Task 1", "Task 2", "Task 3"]


def test_delete_task(page):
    """Delete task using 'x' button."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.delete_task()

    assert not page.query_selector('.main')


def test_delete_clear_completed(page):
    """Clear completed tasks."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.add_task("Task 2")
    todo.add_task("Task 3")
    todo.check_all_completed()
    todo.add_task("Task not completed")
    todo.clear_completed()

    assert todo.get_completed_tasks() == []
    assert todo.get_tasks_left() == 1


def test_edit_by_enter(page):
    """Test function: edit by 'Enter'."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.edit_by_enter("Task 1", "Task 1 Updated")
    page.wait_for_timeout(2000)
    assert todo.get_active_task()[0] == "Task 1 Updated"


def test_delete_by_edit(page):
    """Delete task by editing field to ' '."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.delete_task_by_edit("Task 1")

    assert not page.query_selector(".todo-list")

    
# def test_filter_all(page):
# def test_filter_active(page):
# def test_filter_complete(page):

def test_clear_competed(page):
    """Delete completed tasks by 'clear completed'"""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.add_task("Task 2")
    todo.add_task("Task 3")
    todo.check_all_completed()
    assert todo.get_tasks_left() == 0
    todo.clear_completed()

    assert not page.query_selector(".todo-list")


def test_delete_completed_edit(page):
    """Delete completed task by editing to ' '."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.check_task("Task 1")
    page.get_by_role("link", name="Completed").click()
    todo.delete_task_by_edit("Task 1")

    assert not page.query_selector(".todo-list")


def test_delete_completed_button(page):
    """Delete completed task by 'x' button."""
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")
    todo.add_task("Task 1")
    todo.check_task("Task 1")
    page.get_by_role("link", name="Completed").click()
    todo.delete_task()
    time.sleep(3)

    assert not page.query_selector(".todo-list")

# def test_clear_active(page)
# def test_delete_active_edit(page):
# def test_delete_active_button(page):