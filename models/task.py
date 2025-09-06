class Task:
    all = []

    def __init__(self, title, project, status="incomplete"):
        self.title = title
        self.project = project
        self.status = status
        Task.all.append(self)

    def serialize(self):
        return {"title": self.title, "project": self.project.title, "status": self.status}
    
    def complete(self):
        self.status = "complete"