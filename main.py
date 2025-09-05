from models.project import Project
from models.task import Task
from models.user import User

def main():
    user1 = User("Alice", "alice@flatiron.edu")
    print(user1.name, user1.email)
    project1 = Project("CLI Tool", "project management tool", "09/06/2025")
    print(project1.title, project1.description, project1.due_date)
    task1 = Task("Build classes", "incomplete", user1)
    print(task1.title, task1.status, task1.assigned_to.name)
if __name__ == "__main__":
    main()