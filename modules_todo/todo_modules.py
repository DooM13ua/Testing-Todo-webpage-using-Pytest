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
        self.page.dblclick(f"//label[text()='{old_name}']")
        for i in range(3):
            self.page.click(".edit")
        self.page.keyboard.press("Control+A")
        self.page.keyboard.type(new_name)
        self.page.keyboard.press("Enter")

    def check_task(self, task_name):
        checkbox_selector = (
            "//input[@class='toggle' and "
            f"following-sibling::label[contains(text(), \"{task_name}\")]]"
        )
        self.page.check(checkbox_selector)

    def uncheck_task(self, task_name):
        task = f"//label[contains(text(), '{task_name}')]"
        self.page.uncheck(task + "/preceding-sibling::input[@type='checkbox']")

    def check_all_completed(self):
        # Make all tasks completed.
        self.page.check("//input[@id='toggle-all']")

    def uncheck_all_completed(self):
        # Make all tasks active.
        self.page.uncheck("//input[@id='toggle-all']")

    def delete_task(self):
        self.page.evaluate('''() => {
            const button = document.querySelector('.destroy');
            button.style.display = 'block'; 
        }''')
        self.page.click('.destroy')

    def delete_task_by_edit(self, task_name):
        self.page.dblclick(f"//label[contains(text(), '{task_name}')]")
        self.page.click(".edit")
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

    def get_tasks_left(self):
        return int(self.page.inner_text(".todo-count strong"))