class ToDo:
    def __init__(self, page):
        self.page = page

    def visit(self, url):
        self.page.goto(url)

    def add_task(self, task_name):
        self.page.get_by_placeholder("What needs to be done?").click()
        self.page.get_by_placeholder("What needs to be done?").fill(task_name)
        self.page.get_by_placeholder("What needs to be done?").press("Enter")

    def edit_by_enter(self, old_name, new_name):
        task_field = self.page.locator(f"//label[text()='{old_name}']")
        task_field.dblclick()
        li_element = self.page.locator(f"//label[text()='{old_name}']/ancestor::li")
        edit_element = li_element.locator(".edit")
        edit_element.click()
        self.page.keyboard.press("Control+A")
        self.page.keyboard.type(new_name)
        self.page.keyboard.press("Enter")

    def edit_by_tab(self, old_name, new_name):
        task_field = self.page.locator(f"//label[text()='{old_name}']")
        task_field.dblclick()
        li_element = self.page.locator(f"//label[text()='{old_name}']/ancestor::li")
        edit_element = li_element.locator(".edit")
        edit_element.click()
        self.page.keyboard.press("Control+A")
        self.page.keyboard.type(new_name)
        self.page.keyboard.press("Tab")

    def edit_by_click(self, old_name, new_name):
        task_field = self.page.locator(f"//label[text()='{old_name}']")
        task_field.dblclick()
        li_element = self.page.locator(f"//label[text()='{old_name}']/ancestor::li")
        edit_element = li_element.locator(".edit")
        edit_element.click()
        self.page.keyboard.press("Control+A")
        self.page.keyboard.type(new_name)
        outside = "//h1"
        self.page.click(outside)

    def edit_by_esc(self, old_name, new_name):
        task_field = self.page.locator(f"//label[text()='{old_name}']")
        task_field.dblclick()
        li_element = self.page.locator(f"//label[text()='{old_name}']/ancestor::li")
        edit_element = li_element.locator(".edit")
        edit_element.click()
        self.page.keyboard.press("Control+A")
        self.page.keyboard.type(new_name)
        self.page.keyboard.press("Escape")

    def check_task(self, task_name):
        checkbox_selector = (
            "//input[@class='toggle' and "
            f"following-sibling::label[contains(text(), \"{task_name}\")]]"
        )
        self.page.check(checkbox_selector)

    def uncheck_task(self, task_name):
        checkbox_selector = (
            "//input[@class='toggle' and "
            f"following-sibling::label[contains(text(), \"{task_name}\")]]"
        )
        self.page.uncheck(checkbox_selector)

    def check_all_completed(self):
        # Make all tasks completed.
        self.page.check("//input[@id='toggle-all']")

    def uncheck_all_completed(self):
        # Make all tasks active.
        self.page.uncheck("//input[@id='toggle-all']")

    def delete_task(self, task_name):
        self.page.click(f'.todo-list li label:has-text("{task_name}")')
        self.page.click(f'.todo-list li label:has-text("{task_name}") + .destroy')

    def delete_task_by_edit(self, task_name):
        task_field = self.page.locator(f"//label[text()='{task_name}']")
        task_field.dblclick()
        li_element = self.page.locator(f"//label[text()='{task_name}']/ancestor::li")
        edit_element = li_element.locator(".edit")
        edit_element.click()
        self.page.keyboard.press("Control+A")
        self.page.keyboard.press("Backspace")
        self.page.keyboard.press("Enter")

    def clear_completed(self):
        self.page.query_selector(".clear-completed").click()

    def get_completed_tasks(self):
        completed_tasks = self.page.query_selector_all('.completed .view label')
        return [label.text_content() for label in completed_tasks]

    def get_active_task(self):
        selector = "li[class=' '] > div.view > label"
        active_tasks = self.page.query_selector_all(selector)
        return [task.text_content().strip() for task in active_tasks]

    def get_all_task(self):
        all_task = self.page.query_selector_all("li > div.view > label")
        return [label.text_content() for label in all_task]

    def get_tasks_left(self):
        return int(self.page.inner_text(".todo-count strong"))

    def filter_active(self):
        self.page.get_by_role("link", name="Active").click()

    def filter_complete(self):
        self.page.get_by_role("link", name="Completed").click()

    def filter_all(self):
        self.page.get_by_role("link", name="All").click()