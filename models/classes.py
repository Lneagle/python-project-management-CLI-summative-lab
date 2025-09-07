class User:
    all = {}

    def __init__(self, name, email):
        self.name = name
        self.email = email
        User.all[name] = self

    def serialize(self):
        return {"name": self.name, "email": self.email}
    
    def projects(self):
        return [project for project in Project.all.values() if project.assigned_to == self]
    
class Task:
    all = {}

    def __init__(self, title, project, status="incomplete"):
        self.title = title
        self.project = project
        self.status = status
        Task.all[title] = self

    @property
    def project(self):
        return self._project
    
    @project.setter
    def project(self, value):
        if isinstance(value, Project):
            self._project = value
        else:
            print(f"{value} is not a project")

    def serialize(self):
        return {"title": self.title, "project": self.project.title, "status": self.status}
    
    def complete(self):
        self.status = "complete"

class Project:
    all = {}

    def __init__(self, title, description, assigned_to, due_date):
        self.title = title
        self.description = description
        self.assigned_to = assigned_to
        self.due_date = due_date
        Project.all[title] = self

    @property
    def assigned_to(self):
        return self._assigned_to
    
    @assigned_to.setter
    def assigned_to(self, value):
        if isinstance(value, User):
            self._assigned_to = value
        else:
            print(f"{value} is not a user")

    def serialize(self):
        return {"title": self.title, "description": self.description, "assigned_to": self.assigned_to.name, "due_date": self.due_date}
    
    def tasks(self):
        return [task for task in Task.all.values() if task.project == self]