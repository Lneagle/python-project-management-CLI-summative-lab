from models.project import Project
from models.task import Task
from models.user import User
from utils.filewriter import filewriter as fwrite
import json
import typer

# Setup
USERS_PATH = "data/users.json"
PROJECTS_PATH = "data/projects.json"
TASKS_PATH = "data/tasks.json"

try:
    with open(USERS_PATH, "r") as file:
        data = json.load(file)
        users = []
        for user in data:
            users.append(User(user["name"], user["email"]))
except FileNotFoundError:
    users = []
try:
    with open(PROJECTS_PATH, "r") as file:
        data = json.load(file)
        projects = []
        for project in data:
            project_user = [user for user in User.all if user.name == project["assigned_to"]][0]
            projects.append(Project(project["title"], project["description"], project_user, project["due_date"]))
except FileNotFoundError:
    projects = []
try:
    with open(TASKS_PATH, "r") as file:
        data = json.load(file)
        tasks = []
        for task in data:
            task_project = [project for project in Project.all if project.title == task["project"]][0]
            tasks.append(Task(task["title"], task_project, task["status"]))
except FileNotFoundError:
    tasks = []

# CLI functions
app = typer.Typer()

@app.command()
def add_user(name: str, email: str):
    users.append(User(name, email))
    print(f"User {name} created")
    fwrite(USERS_PATH, users)

@app.command()
def add_project(title: str, description: str, username: str, due_date: str):
    project_user = [user for user in User.all if user.name == username][0]
    projects.append(Project(title, description, project_user, due_date))
    print(f"Project '{title}' created and assigned to {username}")
    fwrite(PROJECTS_PATH, projects)

@app.command()
def add_task(title: str, projectname: str):
    task_project = [project for project in Project.all if project.title == projectname][0]
    tasks.append(Task(title, task_project))
    print(f"Task '{title}' created and assigned to '{projectname}'")
    fwrite(TASKS_PATH, tasks)

@app.command()
def list_users():
    for user in users:
        print(f"Name: {user.name}, email: {user.email}")

@app.command()
def list_projects(assignee: str = "all"):
    if assignee == "all":
        for project in projects:
            print(f"{project.title} | {project.description} | Assignee: {project.assigned_to.name} | Due: {project.due_date}")
    else:
        print(f"{assignee}'s projects:")
        for project in projects:
            if project.assigned_to.name == assignee:
                print(f"{project.title} | {project.description} | Due: {project.due_date}")

@app.command()
def list_tasks(project: str = "all"):
    if project == "all":
        for task in tasks:
            print(f"{task.title} | Project: {task.project.title} | Status: {task.status}")
    else:
        print(f"Tasks for project '{project}':")
        for task in tasks:
            if task.project.title == project:
                print(f"{task.title} | Status: {task.status}")

@app.command()
def complete_task(title: str):
    task_to_complete = [task for task in Task.all if task.title == title][0]
    task_to_complete.complete()
    print(f"{title} completed!")

if __name__ == "__main__":
    app()