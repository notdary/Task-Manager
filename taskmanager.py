import json
from datetime import datetime

print("Welcome to the Task Manager!")

while True:
    print("What would you like to do?")
    print("\n1. Add a task\n2. View tasks\n3. Mark complete\n4. Exit")

    today = datetime.now().date()

    choice = input("Enter your choice: ")

    if choice == "1":
        task_name = input("Enter the name of the task: ").lower()
        task_description = input("What would you like to do? ")
        task_due_date = input("When is the task due? (YYYY-MM-DD): ")
    
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
            print("Task added successfully!")
            
    elif choice == "2":
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
        except FileNotFoundError:
            tasks = []
            print("No tasks found.")
        
        print("How would you like to view the tasks?")
        print("\n1. View all tasks\n2. View tasks that are due\n3. View tasks that are overdue\n4. View tasks that are completed\n5. View task by name.")
        view_choice = input("Enter your choice: ")
        
        due_tasks = []
        overdue_tasks = []
        completed_tasks = []
        
        for task in tasks:
            task_due_date = datetime.fromisoformat(task["due_date"]).date()
            if task["completed"]:
                completed_tasks.append(task)
            elif task_due_date == today:
                due_tasks.append(task)
            elif task_due_date < today:
                overdue_tasks.append(task)
        
        if view_choice == "1":
            for task in tasks:
                print(f"\nName: {task['name']}\nDescription: {task['description']}\nDue date: {task['due_date']}\nCreated at: {task['created_at']}")
        elif view_choice == "2":
            for task in due_tasks:
                print(f"\nName: {task['name']}\nDescription: {task['description']}\nDue date: {task['due_date']}\nCreated at: {task['created_at']}")
        elif view_choice == "3":
            for task in overdue_tasks:
                print(f"\nName: {task['name']}\nDescription: {task['description']}\nDue date: {task['due_date']}\nCreated at: {task['created_at']}")
        elif view_choice == "4":
            for task in completed_tasks:
                print(f"\nName: {task['name']}\nDescription: {task['description']}\nDue date: {task['due_date']}\nCreated at: {task['created_at']}")
        else:
            name = input("What task do you want to find? ")
            found = False
            for task in tasks:
                if task["name"] == name:
                    print(f"\nName: {task['name']}\nDescription: {task['description']}\nDue date: {task['due_date']}\nCreated at: {task['created_at']}")
                    found = True
            if not found:
                found = False
                print("Sorry, we couldn't find task with that name.")
                
    elif choice == "3":
        try:
            with open("tasks.json", "r") as file:
                tasks = json.load(file)
        except FileNotFoundError:
            tasks = []
        
        for i, task in enumerate(tasks):
            status = "✅" if task.get("completed") else "❌"
            print(f"{i+1}. {task['name']} ({status}) - due {task['due_date']}")
        
        idx = int(input("Which task number to mark complete? ")) - 1
        if 0 <= idx < len(tasks):
            tasks[idx]["completed"] = True
            with open("tasks.json", "w") as file:
                json.dump(tasks, file, indent=4)
            print("Task was completed.")

    elif choice == "4":
        print("Bye!")
        break

    else:
        print("Invalid choice, try again!")
        