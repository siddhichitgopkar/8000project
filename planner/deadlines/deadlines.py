import json
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table

console = Console()

def save_deadlines(deadlines):
    """Save the list of deadlines to a JSON file."""
    with open("deadlines/deadlines.json", "w") as f:
        json.dump(deadlines, f)

def load_deadlines():
    """Load the list of deadlines from a JSON file."""
    try:
        with open("deadlines/deadlines.json", "r") as f:
            return sorted(json.load(f), key=lambda x: x['due_date'])
    except FileNotFoundError:
        return []

def add_deadline():
    """Add a new deadline."""
    name = console.input("Enter the name of the assignment/test: ")
    due_date_input = console.input("Enter the due date (e.g., August 13): ")
    
    # Automatically use the current year
    current_year = datetime.now().year
    due_date_str = f"{due_date_input} {current_year}"
    
    try:
        due_date = datetime.strptime(due_date_str, "%B %d %Y").date()
    except ValueError:
        console.print("[bold red]Invalid date format. Please try again.[/bold red]")
        return
    
    deadlines = load_deadlines()
    deadlines.append({"name": name, "due_date": due_date.strftime("%Y-%m-%d")})
    deadlines = sorted(deadlines, key=lambda x: x['due_date'])
    save_deadlines(deadlines)
    console.print("[bold green]Deadline added successfully![/bold green]")

def display_deadlines():
    """Display all deadlines sorted by date."""
    deadlines = load_deadlines()
    today = datetime.today().date()
    tomorrow = today + timedelta(days=1)

    if not deadlines:
        console.print("[bold yellow]No deadlines found.[/bold yellow]")
        return

    table = Table(title="Deadlines", show_header=True, header_style="bold magenta")
    table.add_column("Assignment/Test", style="bold white")
    table.add_column("Due Date", style="bold white")

    for deadline in deadlines:
        due_date = datetime.strptime(deadline['due_date'], "%Y-%m-%d").date()
        if due_date == tomorrow:
            # Highlight the entire row in pink and set the text color to white
            table.add_row(
                f"[bold white on #FF69B4]{deadline['name']}[/bold white on #FF69B4]",
                f"[bold white on #FF69B4]{deadline['due_date']}[/bold white on #FF69B4]"
            )
        else:
            table.add_row(deadline['name'], deadline['due_date'])

    console.print(table)
