import json
from datetime import datetime

print("Welcome to the Task Manager!")

while True:
    print("\nWhat would you like to do?")
    print("\n1. Add a task\n2. View tasks\n3. Mark complete\n4. Exit")

    today = datetime.now().date()

    choice = input("\nEnter your choice: ")

    if choice == "1":
        task_name = input("\nEnter the name of the task: ").upper()
        task_description = input("Enter the description of the task: ")
        
        while True:
            task_due_date = input("Enter the task due date (YYYY-MM-DD): ")
            try:
                datetime.strptime(task_due_date, "%Y-%m-%d")
                break
            except ValueError:
                print("\nInvalid date format, please try again")
            
        task = {
            "name": task_name,
            "description": task_description,
            "due_date": task_due_date,
            "created_at": datetime.now().isoformat(),
            "completed": False
        }
    
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
        except FileNotFoundError:
            tasks = []
        
        tasks.append(task)
        
        with open("tasks.json", "w") as file:
            json.dump(tasks, file, indent=4)
            print("\nTask added successfully!")
            
    elif choice == "2":
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
        except FileNotFoundError:
            tasks = []
            print("\nNo tasks found.")
        
        print("How would you like to view the tasks?")
        print("\n1. View all tasks\n2. View tasks that are due\n3. View tasks that are overdue\n4. View tasks that are completed\n5. View task by name.")
        view_choice = input("\nEnter your choice: ")
        
        due_tasks = []
        overdue_tasks = []
        completed_tasks = []
        
        try:
            for task in tasks:
                task_due_date = datetime.fromisoformat(task["due_date"]).date()
                if task["completed"]:
                    completed_tasks.append(task)
                elif task_due_date == today:
                    due_tasks.append(task)
                elif task_due_date < today:
                    overdue_tasks.append(task)
        except ValueError:
            print(f"\nWARNING: Task {task['name']} has invalid date format: {task['due_date']}")
            
        def display_task(task):
            status = "✅" if task["completed"] else "❌"
            print(f"\nName: {task['name']}\nDescription: {task['description']}\nDue date: {task['due_date']}\nCreated at: {task['created_at']}\nStatus: {status}")
        
        if view_choice == "1":
            for task in tasks:
                display_task(task)
        elif view_choice == "2":
            for task in due_tasks:
                display_task(task)
        elif view_choice == "3":
            for task in overdue_tasks:
                display_task(task)
        elif view_choice == "4":
            for task in completed_tasks:
                display_task(task)
        else:
            name = input("\nWhat task do you want to find? ").upper()
            found = False
            for task in tasks:
                if task["name"] == name:
                    display_task(task)
                    found = True
            if not found:
                found = False
                print("\nSorry, we couldn't find task with that name.")
                
    elif choice == "3":
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
        except FileNotFoundError:
            tasks = []
        
        for i, task in enumerate(tasks):
            status = "✅" if task.get("completed") else "❌"
            print(f"{i+1}. {task['name']} ({status}) - due {task['due_date']}")
        
        try:
            idx = int(input("\nWhich task number to mark complete? ")) - 1
            if 0 <= idx < len(tasks):
                tasks[idx]["completed"] = True
                with open("tasks.json", "w") as file:
                    json.dump(tasks, file, indent=4)
                print("\nTask was completed.")
            else:
                print("\nInvalid task number")
        except ValueError:
            print("\nPlease enter a valid number")

    elif choice == "4":
        print("Bye!")
        break

    else:
        print("\nInvalid choice, try again!")  