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
        for user in data:
            User(user["name"], user["email"])
except FileNotFoundError as error:
    print("An exception occurred: ", error)
try:
    with open(PROJECTS_PATH, "r") as file:
        data = json.load(file)
        for project in data:
            project_user = [user for user in User.all if user.name == project["assigned_to"]][0]
            Project(project["title"], project["description"], project_user, project["due_date"])
except FileNotFoundError as error:
    print("An exception occurred: ", error)
try:
    with open(TASKS_PATH, "r") as file:
        data = json.load(file)
        for task in data:
            task_project = [project for project in Project.all if project.title == task["project"]][0]
            Task(task["title"], task_project, task["status"])
except FileNotFoundError as error:
    print("An exception occurred: ", error)

# CLI functions
app = typer.Typer()

@app.command()
def add_user(name: str, email: str):
    User(name, email)
    print(f"User {name} created")
    fwrite(USERS_PATH, User.all)

@app.command()
def add_project(title: str, description: str, username: str, due_date: str):
    project_user = [user for user in User.all if user.name == username][0]
    Project(title, description, project_user, due_date)
    print(f"Project '{title}' created and assigned to {username}")
    fwrite(PROJECTS_PATH, Project.all)

@app.command()
def add_task(title: str, projectname: str):
    task_project = [project for project in Project.all if project.title == projectname][0]
    Task(title, task_project)
    print(f"Task '{title}' created and assigned to '{projectname}'")
    fwrite(TASKS_PATH, Task.all)

@app.command()
def list_users():
    for user in User.all:
        print(f"Name: {user.name}, email: {user.email}")

@app.command()
def list_projects(assignee: str = "all"):
    if assignee == "all":
        for project in Project.all:
            print(f"{project.title} | {project.description} | Assignee: {project.assigned_to.name} | Due: {project.due_date}")
    else:
        print(f"{assignee}'s projects:")
        for project in Project.all:
            if project.assigned_to.name == assignee:
                print(f"{project.title} | {project.description} | Due: {project.due_date}")

@app.command()
def list_tasks(project: str = "all"):
    if project == "all":
        for task in Task.all:
            print(f"{task.title} | Project: {task.project.title} | Status: {task.status}")
    else:
        print(f"Tasks for project '{project}':")
        for task in Task.all:
            if task.project.title == project:
                print(f"{task.title} | Status: {task.status}")

@app.command()
def complete_task(title: str):
    task_to_complete = [task for task in Task.all if task.title == title][0]
    task_to_complete.complete()
    print(f"{title} completed!")
    fwrite(TASKS_PATH, Task.all)
    
if __name__ == "__main__":
    app()