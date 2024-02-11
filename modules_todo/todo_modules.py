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
        self.page.dblclick(f"//label[contains(text(), '{old_name}')]")
        self.page.click(".edit")
        self.page.keyboard.press("Control+A")
        self.page.keyboard.type(new_name)
        self.page.keyboard.press("Enter")
    # def edit_by_tab(self, old_name, new_name):
    # def edit_by_click_outside(self, old_name, new_name):
    # def edit_by_cancel_edit_by_esc(self, old_name, new_name):

    def update_task(self, old_name, new_name):
        selector = f"//label[contains(text(), '{old_name}')]"
        self.page.click(selector)
        self.page.dblclick(selector)
        self.page.keyboard.press("Control+A")
        self.page.keyboard.type(new_name)
        self.page.keyboard.press("Enter")

    def check_task(self, task_name):
        task = f"//label[contains(text(), '{task_name}')]"
        self.page.check(task + "/preceding-sibling::input[@type='checkbox']")

    def uncheck_task(self, task_name):
        task = f"//label[contains(text(), '{task_name}')]"
        self.page.uncheck(task + "/preceding-sibling::input[@type='checkbox']")

    def delete_task(self):
        self.page.query_selector(".destroy").click()

    def get_completed_tasks(self):
        completed_tasks = self.page.query_selector_all('.completed .view label')
        return [label.text_content() for label in completed_tasks]

    def get_active_task(self):
        selector = "li[class=' '] > div.view > label"
        active_tasks = self.page.query_selector_all(selector)
        return [task.text_content().strip() for task in active_tasks]

    def get_tasks_left(self):
        return int(self.page.inner_text(".todo-count strong"))

    def check_all_completed(self):
        self.page.check("//input[@id='toggle-all']")

    def uncheck_all_completed(self):
        self.page.uncheck("//input[@id='toggle-all']")