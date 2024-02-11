import pytest
from modules_todo.todo_modules import ToDo
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="module")
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        yield page
        browser.close()


def test_end_to_end_positive(page):
    todo = ToDo(page)
    todo.visit("https://todomvc.com/examples/emberjs/todomvc/dist/")

    # 1.Add todos: a, b, c, d, e.
    todo.add_task("a")
    todo.add_task("b")
    todo.add_task("c")
    todo.add_task("d")
    todo.add_task("e")

    # 2.Assert.
    assert todo.get_active_task() == ["a", "b", "c", "d", "e"]
    assert todo.get_tasks_left() == 5

    # 3.Update item "a" as "a-update".
    todo.edit_by_enter("a", "a-update")

    # 4.Assert.
    assert todo.get_active_task() == ["a-update", "b", "c", "d", "e"]
    assert todo.get_tasks_left() == 5

    # 5.Check completed 'b' todos.
    todo.check_task("b")

    # 6.Assert.
    assert todo.get_tasks_left() == 4
    assert todo.get_completed_tasks() == ["b"]
    assert todo.get_active_task() == ["a-update", "c", "d", "e"]

    # 7.Check completed a-update, c.
    todo.check_task("a-update")
    todo.check_task("c")

    # 8.Assert
    assert todo.get_completed_tasks() == ["a-update", "b", "c"]
    assert todo.get_active_task() == ["d", "e"]
    assert todo.get_tasks_left() == 2

    # 9. Check completed, filtration active.
    todo.filter_active()
    page.wait_for_timeout(3000)

    # 10. Assert
    assert todo.get_active_task() == ["d", "e"]
    assert not todo.get_active_task() == ["a-update", "b", "c"]
    assert todo.get_tasks_left() == 2

    # 11. Filtration todos: completed.
    todo.filter_complete()

    # 12. Assert
    assert not todo.get_active_task() == ["d", "e"]
    assert todo.get_completed_tasks() == ["a-update", "b", "c"]
    assert todo.get_tasks_left() == 2

    # 13. Check complete todos, filtration todos "all", delete a-update.
    todo.filter_all()
    todo.check_all_completed()
    todo.delete_task("a-update")

    # 14. Assert
    assert todo.get_tasks_left() == 0
    assert todo.get_completed_tasks() == ["b", "c", "d", "e"]
    assert todo.get_active_task() == []
    assert not todo.get_all_task() == ["a-update"]

    # 15. Uncheck completed todos 'c', delete 'b'.
    todo.uncheck_task("c")
    todo.delete_task("b")

    # 16. Assert.
    assert todo.get_active_task() == ["c"]
    assert todo.get_completed_tasks() == ["d", "e"]
    assert not todo.get_all_task() == ["b"]

    # 17. Clear completed todos.
    todo.clear_completed()

    # 18. Assert.
    assert todo.get_active_task() == ["c"]
    assert not todo.get_all_task() == ["d", "e"]

    # 19. Add todos f,g,h,i.
    todo.add_task("f")
    todo.add_task("g")
    todo.add_task("h")
    todo.add_task("i")

    # 20. Assert.
    assert todo.get_active_task() == ["c", "f", "g", "h", "i"]
    assert todo.get_tasks_left() == 5

    # 21. Check completed c, f, g, h, i
    todo.check_task("c")
    todo.check_task("f")
    todo.check_task("g")
    todo.check_task("h")
    todo.check_task("i")

    # 22. Assert.
    assert todo.get_completed_tasks() == ["c", "f", "g", "h", "i"]
    assert todo.get_tasks_left() == 0
    assert todo.get_active_task() == []

    # 23. Uncheck complete all.
    todo.uncheck_all_completed()

    # 24. Assert
    assert todo.get_active_task() == ["c", "f", "g", "h", "i"]
    assert todo.get_tasks_left() == 5
    assert todo.get_completed_tasks() == []

