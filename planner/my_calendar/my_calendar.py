from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
import json
import os
import re  # Importing the 're' module for regular expressions

console = Console()

# File to store calendar data
CALENDAR_FILE = "calendar_data.json"

def load_calendar():
    """Load calendar data from a JSON file."""
    if os.path.exists(CALENDAR_FILE):
        try:
            with open(CALENDAR_FILE, 'r') as f:
                calendar_data = json.load(f)
                for event in calendar_data:
                    event["start_time"] = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M:%S.%f")
                    event["end_time"] = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M:%S.%f")
                return calendar_data
        except (json.JSONDecodeError, ValueError) as e:
            console.print(f"[bold red]Error loading calendar data: {e}[/bold red]")
    return []

def save_calendar(calendar_data):
    """Save calendar data to a JSON file."""
    try:
        with open(CALENDAR_FILE, 'w') as f:
            json.dump([
                {
                    "title": event["title"],
                    "start_time": event["start_time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "end_time": event["end_time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "recurrence": event["recurrence"],
                    "completed": event.get("completed", False)  # Save completed status
                } for event in calendar_data
            ], f)
    except IOError as e:
        console.print(f"[bold red]Error saving calendar data: {e}[/bold red]")

def display_calendar(week_start):
    """Display the weekly calendar."""
    calendar_data = load_calendar()
    table = Table(title="Weekly Calendar", show_lines=True, style="bold #FC6C85")
    table.add_column("Time", style="#FC6C85", width=10)
    days = [(week_start + timedelta(days=i)).strftime("%B %d\n%A") for i in range(7)]
    for day in days:
        table.add_column(day, style="#FC6C85", width=20)

    ongoing_events = {}

    for half_hour in range(6 * 2, 24 * 2):  # From 6 AM to 12 AM
        time_label = (datetime.min + timedelta(minutes=half_hour * 30)).time().strftime('%I:%M %p')
        row = [time_label]
        for i in range(7):
            day = week_start + timedelta(days=i)
            block = ""
            time_slot_start = day.replace(hour=(half_hour // 2), minute=(half_hour % 2) * 30)
            time_slot_end = time_slot_start + timedelta(minutes=30)

            for event in calendar_data:
                if event["start_time"] <= time_slot_start < event["end_time"]:
                    event_display = event["title"]
                    style = "bold white on #FF69B4"  # Default style

                    if event.get("completed", False):
                        style = "bold white on #D87093"  # Darker pink for completed tasks

                    if event_display in ongoing_events and ongoing_events[event_display] == event["start_time"]:
                        block = f"[{style}]{' ' * 18}[/{style}]"
                    else:
                        block = f"[{style}]{event_display}{' ' * (18 - len(event_display))}[/{style}]"
                        ongoing_events[event_display] = event["start_time"]
                    break

            row.append(block)
        table.add_row(*row)
    
    console.print(table)

def add_event():
    """Add a new event to the calendar."""
    calendar_data = load_calendar()
    title = console.input("[#FC6C85]Event title: [/#FC6C85]")
    day_time = console.input("[#FC6C85]Enter day and time (e.g., Monday 5:30 PM): [/#FC6C85]")
    duration = int(console.input("[#FC6C85]Enter event duration in minutes: [/#FC6C85]"))
    recurrence = console.input("[#FC6C85]Recurrence (none, daily, weekly, monthly) (default: none): [/#FC6C85]") or "none"
    recurrence_weeks = int(console.input("[#FC6C85]Number of weeks to recur (default: 4): [/#FC6C85]") or 4)

    try:
        day, time = re.match(r"(\w+)\s+(\d{1,2}:\d{2}\s*[APMapm]{2})", day_time).groups()
        time = datetime.strptime(time, "%I:%M %p").time()
        days_of_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        event_day = week_start + timedelta(days=days_of_week[day.capitalize()])
        start_time = datetime.combine(event_day, time)
        end_time = start_time + timedelta(minutes=duration)

        for _ in range(recurrence_weeks):
            calendar_data.append({"title": title, "start_time": start_time, "end_time": end_time, "recurrence": recurrence})
            if recurrence == "daily":
                start_time += timedelta(days=1)
                end_time += timedelta(days=1)
            elif recurrence == "weekly":
                start_time += timedelta(weeks=1)
                end_time += timedelta(weeks=1)
            elif recurrence == "monthly":
                start_time = start_time.replace(month=(start_time.month % 12) + 1)
                end_time = end_time.replace(month=(end_time.month % 12) + 1)
            else:
                break

        save_calendar(calendar_data)
        console.print("[bold #FC6C85]Event added successfully![/bold #FC6C85]")
    except (ValueError, AttributeError):
        console.print("[bold red]Invalid day and time format! Please use the format: Monday 5:30 PM[/bold red]")

def modify_event():
    """Modify an existing event."""
    calendar_data = load_calendar()
    display_event_list()
    try:
        event_id = int(console.input("[#FC6C85]Enter event ID to modify: [/#FC6C85]"))
        if 0 <= event_id < len(calendar_data):
            title = console.input("[#FC6C85]New event title: [/#FC6C85]") or calendar_data[event_id]["title"]
            day_time = console.input("[#FC6C85]New day and time (e.g., Monday 5:30 PM): [/#FC6C85]")
            duration = console.input("[#FC6C85]New event duration in minutes: [/#FC6C85]")
            recurrence = console.input("[#FC6C85]New recurrence (none, daily, weekly, monthly) (default: none): [/#FC6C85]") or calendar_data[event_id]["recurrence"]

            if day_time:
                day, time = re.match(r"(\w+)\s+(\d{1,2}:\d{2}\s*[APMapm]{2})", day_time).groups()
                time = datetime.strptime(time, "%I:%M %p").time()
                days_of_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
                week_start = datetime.now() - timedelta(days=datetime.now().weekday())
                event_day = week_start + timedelta(days=days_of_week[day.capitalize()])
                start_time = datetime.combine(event_day, time)
                calendar_data[event_id]["start_time"] = start_time

                if duration:
                    end_time = start_time + timedelta(minutes=int(duration))
                    calendar_data[event_id]["end_time"] = end_time

            calendar_data[event_id]["title"] = title
            calendar_data[event_id]["recurrence"] = recurrence

            save_calendar(calendar_data)
            console.print("[bold #FC6C85]Event modified successfully![/bold #FC6C85]")
        else:
            console.print("[bold red]Invalid event ID![/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid event ID.[/bold red]")

def remove_event():
    """Remove an event from the calendar."""
    calendar_data = load_calendar()
    display_event_list()
    try:
        event_id = int(console.input("[#FC6C85]Enter event ID to remove: [/#FC6C85]"))
        if 0 <= event_id < len(calendar_data):
            del calendar_data[event_id]
            save_calendar(calendar_data)
            console.print("[bold #FC6C85]Event removed successfully![/bold #FC6C85]")
        else:
            console.print("[bold red]Invalid event ID![/bold red]")
    except ValueError:
        console.print("[bold red]Invalid input! Please enter a valid event ID.[/bold red]")

def display_event_list():
    """Display a list of all events."""
    calendar_data = load_calendar()
    for i, event in enumerate(calendar_data):
        console.print(f"[{i}] {event['title']} on {event['start_time'].strftime('%A %I:%M %p')} to {event['end_time'].strftime('%I:%M %p')}")
