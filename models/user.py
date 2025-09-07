from models.project import Project

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