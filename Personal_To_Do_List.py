import tkinter as tk
from tkinter import messagebox
from datetime import datetime

class Task:
    def __init__(self, description, due_date=None):
        self.description = description
        self.completed = False
        self.due_date = due_date

class TodoListManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Manager")

        self.tasks = []

        # Task Entry (replaced with tk.Text)
        self.task_entry = self.create_text_entry(root, "Enter task description...", width=30, height=3)
        self.task_entry.grid(row=0, column=0, padx=10, pady=10)

        # Due Date Entry
        self.due_date_entry = self.create_entry(root, "DD-MM-YYYY", width=15)
        self.due_date_entry.grid(row=0, column=1, padx=10, pady=10)

        # Add Task Button
        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

        # Task Listbox
        self.task_listbox = tk.Listbox(root, width=50, height=10)
        self.task_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        # Mark Completed Button
        self.mark_completed_button = tk.Button(root, text="Mark Completed", command=self.mark_completed)
        self.mark_completed_button.grid(row=1, column=2, padx=10, pady=10)

        # Delete Task Button
        self.delete_button = tk.Button(root, text="Delete Task", command=self.delete_task)
        self.delete_button.grid(row=2, column=2, padx=5, pady=5)

        # View Tasks OptionMenu
        self.view_var = tk.StringVar(root)
        self.view_var.set("All")
        self.view_optionmenu = tk.OptionMenu(root, self.view_var, "All", "Completed", "Pending", command=self.update_task_listbox)
        self.view_optionmenu.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.view_optionmenu.bind("<Configure>", lambda event: self.update_task_listbox())

    def create_text_entry(self, master, placeholder, width, height):
        entry = tk.Text(master, width=width, height=height)
        self.add_placeholder(entry, placeholder)
        return entry

    def create_entry(self, master, placeholder, width):
        entry = tk.Entry(master, width=width)
        self.add_placeholder(entry, placeholder)
        return entry

    def add_task(self):
        description = self.task_entry.get("1.0", tk.END).strip()
        due_date = self.due_date_entry.get()

        if self.validate_input(description, due_date):
            task = Task(description, due_date)
            self.tasks.append(task)
            self.clear_entries()
        else:
            messagebox.showwarning("Input Error", "Both task description and due date are required.")

        self.update_task_listbox()

    def validate_input(self, description, due_date):
        if not description or description == "Enter task description...":
            messagebox.showwarning("Input Error", "Task description cannot be empty.")
            return False

        if not due_date or due_date == "DD-MM-YYYY":
            messagebox.showwarning("Input Error", "Due date is required.")
            return False

        try:
            datetime.strptime(due_date, "%d-%m-%Y")
        except ValueError:
            messagebox.showwarning("Input Error", "Invalid due date format. Please use DD-MM-YYYY.")
            return False

        return True

    def update_task_listbox(self, *args):
        self.task_listbox.delete(0, tk.END)
        view_option = self.view_var.get()

        for task in self.tasks:
            if view_option == "All" or (view_option == "Completed" and task.completed) or (view_option == "Pending" and not task.completed):
                status = "Completed" if task.completed else "Pending"
                entry = f"{task.description} - {status}, Due: {task.due_date}"
                self.task_listbox.insert(tk.END, entry)

    def clear_entries(self):
        self.task_entry.delete("1.0", tk.END)
        self.due_date_entry.delete(0, tk.END)

    def mark_completed(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            self.tasks[selected_index].completed = True
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            selected_index = int(selected_index[0])
            del self.tasks[selected_index]
            self.update_task_listbox()
        else:
            messagebox.showwarning("Selection Error", "Please select a task to delete.")

    def add_placeholder(self, widget, placeholder):
        widget.insert(tk.END, placeholder)
        widget.bind("<FocusIn>", lambda event, widget=widget, placeholder=placeholder: self.on_focus_in(event, widget, placeholder))
        widget.bind("<FocusOut>", lambda event, widget=widget, placeholder=placeholder: self.on_focus_out(event, widget, placeholder))

    def on_focus_in(self, event, widget, placeholder):
        if isinstance(widget, tk.Text) and widget.get("1.0", tk.END).strip() == placeholder:
            widget.delete("1.0", tk.END)
        elif isinstance(widget, tk.Entry) and widget.get().strip() == placeholder:
            widget.delete(0, tk.END)

    def on_focus_out(self, event, widget, placeholder):
        if isinstance(widget, tk.Text) and not widget.get("1.0", tk.END).strip():
            widget.insert("1.0", placeholder)
        elif isinstance(widget, tk.Entry) and not widget.get().strip():
            widget.insert(0, placeholder)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoListManagerGUI(root)
    root.mainloop()