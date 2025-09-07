from models.task import Task

class Project:
    all = {}

    def __init__(self, title, description, assigned_to, due_date):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.due_date = due_date
        Project.all[title] = self

    def serialize(self):
        return {"title": self.title, "description": self.description, "assigned_to": self.assigned_to.name, "due_date": self.due_date}
    
    def tasks(self):
        return [task for task in Task.all.values() if task.project == self]