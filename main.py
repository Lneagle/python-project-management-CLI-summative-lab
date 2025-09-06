from models.project import Project
from models.task import Task
from models.user import User
import json
import argparse

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


def main():
    #user1 = User("Alice", "alice@flatiron.edu")
    #user2 = User("Bob", "bob@flatiron.edu")
    #users.append(user1.serialize())
    #users.append(user2.serialize())
    #with open(USERS_PATH, "w") as file:
        #json.dump(users, file)
    for user in users:
        print(user.serialize())
        for project in user.projects():
            print(project.serialize())
            for task in project.tasks():
                print(task.serialize())

    #project1 = Project("CLI Tool", "project management tool", users[0], "09/06/2025")
    #projects.append(project1)
    #with open(PROJECTS_PATH, "w") as file:
        #data = []
        #for project in projects:
            #data.append(project.serialize())
        #json.dump(data, file)
    #task1 = Task("Build classes", projects[0])
    #tasks.append(task1)
    #with open(TASKS_PATH, "w") as file:
        #data = []
        #for task in tasks:
            #data.append(task.serialize())
        #json.dump(data, file)
    #print(task1.title, task1.assigned_to.name, task1.status)

    

    
if __name__ == "__main__":
    main()