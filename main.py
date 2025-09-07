from models.classes import User, Project, Task
from utils.filewriter import filewriter as fwrite
import json
import typer

# Setup - reads in previously stored data if available
USERS_PATH = "data/users.json"
PROJECTS_PATH = "data/projects.json"
TASKS_PATH = "data/tasks.json"

try:
    with open(USERS_PATH, "r") as file:
        data = json.load(file)
        for user in data:
            User(user["name"], user["email"])
except FileNotFoundError as error:
    pass
try:
    with open(PROJECTS_PATH, "r") as file:
        data = json.load(file)
        for project in data:
            project_user = User.all.get(project["assigned_to"])
            Project(project["title"], project["description"], project_user, project["due_date"])
except FileNotFoundError as error:
    pass
try:
    with open(TASKS_PATH, "r") as file:
        data = json.load(file)
        for task in data:
            task_project = Project.all.get(task["project"])
            Task(task["title"], task_project, task["status"])
except FileNotFoundError as error:
    pass

# CLI functions
app = typer.Typer()

@app.command()
def add_user(name: str, email: str):
    User(name, email)
    print(f"User {name} created")
    fwrite(USERS_PATH, User.all)

@app.command()
def add_project(title: str, description: str, username: str, due_date: str):
    project_user = User.all.get(username)
    if project_user:
        Project(title, description, project_user, due_date)
        print(f"Project '{title}' created and assigned to {username}")
        fwrite(PROJECTS_PATH, Project.all)
    else:
        print(f"{username} does not exist. Project not created.")

@app.command()
def add_task(title: str, projectname: str):
    task_project = Project.all.get(projectname)
    if (task_project):
        Task(title, task_project)
        print(f"Task '{title}' created and assigned to '{projectname}'")
        fwrite(TASKS_PATH, Task.all)
    else:
        print(f"{projectname} does not exist. Task not created.")

@app.command()
def list_users():
    for user in User.all.values():
        print(f"Name: {user.name}, email: {user.email}")

@app.command()
def list_projects(assignee: str = "all"):
    if assignee == "all":
        for project in Project.all.values():
            print(f"{project.title} | {project.description} | Assignee: {project.assigned_to.name} | Due: {project.due_date}")
    else:
        user = User.all.get(assignee)
        if (user):
            print(f"{assignee}'s projects:")
            for project in user.projects():
                print(f"{project.title} | {project.description} | Due: {project.due_date}")
        else:
            print(f"{assignee} not found")

@app.command()
def list_tasks(project: str = "all"):
    if project == "all":
        for task in Task.all.values():
            print(f"{task.title} | Project: {task.project.title} | Status: {task.status}")
    else:
        proj = Project.all.get(project)
        if (proj):
            print(f"Tasks for project '{project}':")
            for task in proj.tasks():
                print(f"{task.title} | Status: {task.status}")
        else:
            print(f"{project} not found")

@app.command()
def complete_task(title: str):
    task_to_complete = Task.all.get(title)
    if (task_to_complete):
        task_to_complete.complete()
        print(f"{title} completed!")
        fwrite(TASKS_PATH, Task.all)
    else:
        print(f"Task '{title}' not found")

if __name__ == "__main__":
    app()