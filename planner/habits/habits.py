import json
import os
from datetime import datetime
from rich.console import Console
from rich.table import Table

console = Console()
habit_data = []  # List to hold habits
habit_file = "habits_data.json"  # File to store habit data

def load_habits():
    """Load habits from the JSON file."""
    global habit_data
    if os.path.exists(habit_file):
        with open(habit_file, 'r') as f:
            habit_data = json.load(f)

def save_habits():
    """Save habits to the JSON file."""
    with open(habit_file, 'w') as f:
        json.dump(habit_data, f, default=str)

def display_habits():
    """Display all habits with their completion status."""
    load_habits()
    if not habit_data:
        console.print("[bold red]No habits found. Add a new habit![/bold red]")
        return

    table = Table(title="Habits Tracker", show_header=True, header_style="bold magenta", show_lines=True)
    table.add_column("ID", style="bold #FC6C85")
    table.add_column("Habit", style="bold #FC6C85")
    for day in range(1, 32):
        table.add_column(str(day), style="bold #FC6C85")

    for i, habit in enumerate(habit_data):
        habit_row = [str(i), habit["title"]]
        for day in range(1, 32):
            day_str = str(day)
            habit_row.append("[bold #FC6C85]X[/bold #FC6C85]" if day_str in habit["completion"] else "")
        table.add_row(*habit_row)

    console.print(table)

def add_habit():
    """Add a new habit."""
    load_habits()
    title = console.input("[#FC6C85]Habit title: [/#FC6C85]")
    habit_data.append({"title": title, "completion": []})
    save_habits()
    console.print("[bold #FC6C85]Habit added successfully![/bold #FC6C85]")

def delete_habit():
    """Delete an existing habit."""
    load_habits()
    display_habits()
    habit_id = int(console.input("[#FC6C85]Enter habit ID to delete: [/#FC6C85]"))
    if 0 <= habit_id < len(habit_data):
        habit_data.pop(habit_id)
        save_habits()
        console.print("[bold #FC6C85]Habit deleted successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid habit ID![/bold red]")

def mark_habit_done():
    """Mark a habit as done for today."""
    load_habits()
    display_habits()
    habit_id = int(console.input("[#FC6C85]Enter habit ID to mark as done for today: [/#FC6C85]"))
    if 0 <= habit_id < len(habit_data):
        today = str(datetime.now().day)
        if today not in habit_data[habit_id]["completion"]:
            habit_data[habit_id]["completion"].append(today)
        save_habits()
        console.print("[bold #FC6C85]Habit marked as done for today![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid habit ID![/bold red]")
