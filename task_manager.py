import json
import datetime

class Task:
    def __init__(self, description, deadline=None, status="pending"):
        self.description = description
        self.deadline = deadline
        self.status = status
        self.id = self.generate_id() # We'll implement this soon

    def generate_id(self):
        # Generate a unique ID (you can use UUIDs for more robust solutions)
        with open("tasks.json", "r") as f:
            try:
                tasks = json.load(f)
                if tasks:  # Check if the list is not empty
                    max_id = max(task.get("id", 0) for task in tasks)  # Handle missing 'id'
                    return max_id + 1
                else:
                    return 1  # First ID
            except json.JSONDecodeError:
                return 1

    def to_dict(self):  # For JSON serialization
        return {
            "id": self.id,
            "description": self.description,
            "deadline": self.deadline.isoformat() if self.deadline else None,  # Convert date to string (YYYY-MM-DD)
            "status": self.status
        }

    @classmethod
    def from_dict(cls, data):  # For JSON deserialization
        deadline_str = data.get("deadline")
        deadline = datetime.date.fromisoformat(deadline_str) if deadline_str else None # Convert string to date
        task = cls(data["description"], deadline, data["status"])
        task.id = data["id"]
        return task

# ... (rest of the code)

def load_tasks():
    try:
        with open("tasks.json", "r") as f:
            tasks_data = json.load(f)
            return [Task.from_dict(task_data) for task_data in tasks_data]
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_tasks(tasks):
    with open("tasks.json", "w") as f:
        json.dump([task.to_dict() for task in tasks], f, indent=4)

def add_task(tasks):
    description = input("Enter task description: ")
    while True: # loop added to check date format
        deadline_str = input("Enter deadline (YYYY-MM-DD, or leave blank): ")
        try:
            deadline = datetime.datetime.strptime(deadline_str, "%Y-%m-%d").date() if deadline_str else None
            break # if the date is correct the loop will be terminated
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")
    new_task = Task(description, deadline)
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{description}' added with ID: {new_task.id}")

def view_tasks(tasks, filter_status=None):
    for task in tasks:
        if filter_status is None or task.status == filter_status:
            print(f"ID: {task.id}, Description: {task.description}, Deadline: {task.deadline}, Status: {task.status}")

def update_task(tasks):
    task_id = int(input("Enter task ID to update: "))
    for task in tasks:
        if task.id == task_id:
            print("1. Update description")
            print("2. Update status")
            choice = input("Enter your choice: ")
            if choice == '1':
                task.description = input("Enter new description: ")
            elif choice == '2':
                task.status = input("Enter new status (pending/completed): ")
            save_tasks(tasks)
            print("Task updated.")
            return
    print("Task not found.")

def delete_task(tasks):
    task_id = int(input("Enter task ID to delete: "))
    tasks[:] = [task for task in tasks if task.id != task_id] # Efficient removal
    save_tasks(tasks)
    print("Task deleted.")

def main():
    tasks = load_tasks()
    while True:
        print("\nTask Management Menu:")
        print("1. Add a task")
        print("2. View all tasks")
        print("3. View pending tasks")
        print("4. View completed tasks")
        print("5. Update a task")
        print("6. Delete a task")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_task(tasks)
        elif choice == '2':
            view_tasks(tasks)
        elif choice == '3':
            view_tasks(tasks, "pending")
        elif choice == '4':
            view_tasks(tasks, "completed")
        elif choice == '5':
            update_task(tasks)
        elif choice == '6':
            delete_task(tasks)
        elif choice == '7':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()