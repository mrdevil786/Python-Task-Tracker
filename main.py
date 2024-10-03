import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


# Function to load tasks from file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    return []


# Function to save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)


# Function to add a new task with priority and due date
def add_task(tasks):
    task_name = input("Enter the task name: ")
    priority = input("Enter task priority (Low/Medium/High): ")
    due_date = input("Enter due date (YYYY-MM-DD): ")

    # Validate due date input
    try:
        due_date = datetime.strptime(due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError:
        print("Invalid date format. Task will be added without a due date.")
        due_date = None

    tasks.append({
        "task": task_name,
        "priority": priority.capitalize(),
        "due_date": due_date,
        "completed": False
    })
    save_tasks(tasks)
    print(
        f'Task "{task_name}" added with priority {priority.capitalize()} and due date {due_date if due_date else "None"}.'
    )


# Function to view all tasks, optionally filtered and sorted
def view_tasks(tasks, filter_status=None, sort_by=None):
    filtered_tasks = tasks

    # Filter tasks by completion status
    if filter_status == "completed":
        filtered_tasks = [task for task in tasks if task["completed"]]
    elif filter_status == "pending":
        filtered_tasks = [task for task in tasks if not task["completed"]]

    # Sort tasks by due date or priority
    if sort_by == "due_date":
        filtered_tasks = sorted(filtered_tasks,
                                key=lambda x: x["due_date"]
                                if x["due_date"] else "")
    elif sort_by == "priority":
        priority_order = {"Low": 1, "Medium": 2, "High": 3}
        filtered_tasks = sorted(
            filtered_tasks, key=lambda x: priority_order.get(x["priority"], 0))

    if not filtered_tasks:
        print("No tasks found!")
        return

    for i, task in enumerate(filtered_tasks, 1):
        status = "✓" if task["completed"] else "✗"
        due = task["due_date"] if task["due_date"] else "None"
        print(
            f"{i}. {task['task']} - {task['priority']} - Due: {due} - {status}"
        )


# Function to mark task as completed
def complete_task(tasks):
    view_tasks(tasks, filter_status="pending")
    task_num = int(input("Enter the task number to mark as completed: ")) - 1
    if 0 <= task_num < len(tasks):
        tasks[task_num]["completed"] = True
        save_tasks(tasks)
        print(f'Task "{tasks[task_num]["task"]}" marked as completed.')
    else:
        print("Invalid task number.")


# Function to delete a task
def delete_task(tasks):
    view_tasks(tasks)
    task_num = int(input("Enter the task number to delete: ")) - 1
    if 0 <= task_num < len(tasks):
        task = tasks.pop(task_num)
        save_tasks(tasks)
        print(f'Task "{task["task"]}" deleted.')
    else:
        print("Invalid task number.")


# Function to edit a task
def edit_task(tasks):
    view_tasks(tasks)
    task_num = int(input("Enter the task number to edit: ")) - 1
    if 0 <= task_num < len(tasks):
        task = tasks[task_num]
        print(f'Editing task: {task["task"]}')
        new_name = input(
            f"Enter new name (or leave empty to keep '{task['task']}'): ")
        new_priority = input(
            f"Enter new priority (Low/Medium/High) or leave empty to keep '{task['priority']}': "
        )
        new_due_date = input(
            f"Enter new due date (YYYY-MM-DD) or leave empty to keep '{task['due_date']}': "
        )

        task["task"] = new_name or task["task"]
        task["priority"] = new_priority.capitalize() or task["priority"]

        if new_due_date:
            try:
                task["due_date"] = datetime.strptime(
                    new_due_date, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError:
                print("Invalid date format. Due date not changed.")

        save_tasks(tasks)
        print(f'Task "{task["task"]}" updated.')
    else:
        print("Invalid task number.")


# Main function to show menu and handle user input
def task_tracker():
    tasks = load_tasks()
    while True:
        print("\nTask Tracker Menu:")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Complete Task")
        print("4. Edit Task")
        print("5. Delete Task")
        print("6. View Completed Tasks")
        print("7. View Pending Tasks")
        print("8. Sort Tasks by Due Date")
        print("9. Sort Tasks by Priority")
        print("10. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            add_task(tasks)
        elif choice == "2":
            view_tasks(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            edit_task(tasks)
        elif choice == "5":
            delete_task(tasks)
        elif choice == "6":
            view_tasks(tasks, filter_status="completed")
        elif choice == "7":
            view_tasks(tasks, filter_status="pending")
        elif choice == "8":
            view_tasks(tasks, sort_by="due_date")
        elif choice == "9":
            view_tasks(tasks, sort_by="priority")
        elif choice == "10":
            print("Exiting Task Tracker. Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")


# Run the task tracker
if __name__ == "__main__":
    task_tracker()
