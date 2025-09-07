import subprocess
import os

def run_cli_command(command):
    """Helper to run CLI command and capture output"""
    return subprocess.run(command, capture_output=True, text=True)

def test_add_user():
    result = run_cli_command(["python", "-m", "main", "add-user", "Alice", "alice@alice.com"])
    assert "User Alice created" in result.stdout

def test_list_users():
    result = run_cli_command(["python", "-m", "main", "list-users"])
    assert "Name: Alice, email: alice@alice.com" in result.stdout

def test_add_project():
    result = run_cli_command(["python", "-m", "main", "add-project", "Test Project", "Test description", "Alice", "09/22/2025"])
    assert "Project 'Test Project' created and assigned to Alice" in result.stdout

def test_list_projects():
    result = run_cli_command(["python", "-m", "main", "list-projects"])
    assert "Test Project | Test description | Assignee: Alice | Due: 09/22/2025" in result.stdout

def test_list_projects_with_options():
    result = run_cli_command(["python", "-m", "main", "list-projects", "--assignee", "Alice"])
    assert "Test Project | Test description | Due: 09/22/2025" in result.stdout

def test_add_task():
    result = run_cli_command(["python", "-m", "main", "add-task", "Test Task", "Test Project"])
    assert "Task 'Test Task' created and assigned to 'Test Project'" in result.stdout

def test_list_tasks():
    result = run_cli_command(["python", "-m", "main", "list-tasks"])
    assert "Test Task | Project: Test Project | Status: incomplete" in result.stdout

def test_list_tasks_with_options():
    result = run_cli_command(["python", "-m", "main", "list-tasks", "--project", "Test Project"])
    assert "Test Task | Status: incomplete" in result.stdout
    
def test_complete_task():
    result = run_cli_command(["python", "-m", "main", "complete-task", "Test Task"])
    assert "Test Task completed!" in result.stdout

def test_list_tasks_completed():
    result = run_cli_command(["python", "-m", "main", "list-tasks"])
    assert "Test Task | Project: Test Project | Status: complete" in result.stdout