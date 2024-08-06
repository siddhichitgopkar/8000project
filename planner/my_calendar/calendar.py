import json
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
import re

console = Console()
calendar_data = []  # List to hold calendar events
calendar_file = "calendar_data.json"  # File to store calendar data

def load_calendar():
    """Load calendar data from the JSON file."""
    global calendar_data
    if os.path.exists(calendar_file):
        with open(calendar_file, 'r') as f:
            calendar_data = json.load(f)
            # Convert string dates back to datetime objects
            for event in calendar_data:
                event["start_time"] = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M:%S.%f")
                event["end_time"] = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M:%S.%f")

def save_calendar():
    """Save calendar data to the JSON file."""
    with open(calendar_file, 'w') as f:
        json.dump(calendar_data, f, default=str)

def display_calendar(week_start):
    """Display the weekly calendar with events."""
    load_calendar()
    table = Table(title="Weekly Calendar", show_lines=True, style="bold #FC6C85")
    
    # Create time column
    table.add_column("Time", style="#FC6C85", width=8)
    
    # Create columns for each day of the week
    days = [(week_start + timedelta(days=i)).strftime("%B %d\n%A") for i in range(7)]
    for day in days:
        table.add_column(day, style="#FC6C85", width=16)

    # Initialize empty rows for each 15-minute slot from 6 AM to 12 AM
    time_slots = [(datetime.min + timedelta(minutes=15 * i)).strftime('%I:%M %p') for i in range(6 * 4, 24 * 4)]
    rows = [[""] * 7 for _ in time_slots]

    # Create a dictionary to hold the events for each day
    day_events = {day: [] for day in days}
    for event in calendar_data:
        event_day = event["start_time"].strftime("%B %d\n%A")
        if event_day in day_events:
            day_events[event_day].append(event)

    # Sort the events for each day by their start time
    for day in day_events:
        day_events[day].sort(key=lambda e: e["start_time"])

    # Place events in the appropriate rows
    for day_idx, day in enumerate(days):
        events = day_events[day]
        for event in events:
            start_index = (event["start_time"].hour - 6) * 4 + event["start_time"].minute // 15
            duration = int((event["end_time"] - event["start_time"]).total_seconds() / 60 // 15)
            event_str = f"{event['title']}"
            for i in range(duration):
                if i == 0:
                    rows[start_index + i][day_idx] = f"[bold on #FC6C85 white]{event_str:<15}[/bold on #FC6C85 white]"
                else:
                    rows[start_index + i][day_idx] = f"[on #FC6C85]{'|':<15}[/on #FC6C85]"  # Continue the block

    # Add time slots and rows to the table
    for time_slot, row in zip(time_slots, rows):
        table.add_row(time_slot, *row)

    console.print(table)

def display_event_list():
    """Display a list of all events."""
    load_calendar()
    for i, event in enumerate(calendar_data):
        console.print(f"[{i}] {event['title']} on {event['start_time'].strftime('%A %I:%M %p')} to {event['end_time'].strftime('%I:%M %p')}")

def add_event():
    """Add a new event to the calendar."""
    load_calendar()
    title = console.input("[#FC6C85]Event title: [/#FC6C85]")
    day_time = console.input("[#FC6C85]Enter day and time (e.g., Monday 5:30 PM): [/#FC6C85]")
    duration = int(console.input("[#FC6C85]Enter event duration in minutes: [/#FC6C85]"))
    recurrence = console.input("[#FC6C85]Recurrence (none, daily, weekly, monthly) (default: none): [/#FC6C85]") or "none"

    # Parse the day and time input
    match = re.match(r"(\w+)\s+(\d{1,2}:\d{2}\s*[APMapm]{2})", day_time)
    if match:
        day, time = match.groups()
        time = datetime.strptime(time, "%I:%M %p")
        day = day.capitalize()

        # Map the day of the week to an integer
        days_of_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        event_day = week_start + timedelta(days=days_of_week[day])

        # Create start and end times for the event
        start_time = event_day.replace(hour=time.hour, minute=time.minute)
        end_time = start_time + timedelta(minutes=duration)
        # Add the event to the calendar data
        calendar_data.append({"title": title, "start_time": start_time, "end_time": end_time, "recurrence": recurrence})
        save_calendar()
        console.print("[bold #FC6C85]Event added successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid day and time format! Please use the format: Monday 5:30 PM[/bold red]")

def modify_event():
    """Modify an existing event in the calendar."""
    load_calendar()
    display_event_list()
    event_id = int(console.input("[#FC6C85]Enter event ID to modify: [/#FC6C85]"))
    if 0 <= event_id < len(calendar_data):
        title = console.input("[#FC6C85]New event title: [/#FC6C85]") or calendar_data[event_id]["title"]
        day_time = console.input("[#FC6C85]New day and time (e.g., Monday 5:30 PM): [/#FC6C85]")
        duration = console.input("[#FC6C85]New event duration in minutes: [/#FC6C85]")
        recurrence = console.input("[#FC6C85]New recurrence (none, daily, weekly, monthly) (default: none): [/#FC6C85]") or calendar_data[event_id]["recurrence"]

        if day_time:
            match = re.match(r"(\w+)\s+(\d{1,2}:\d{2}\s*[APMapm]{2})", day_time)
            if match:
                day, time = match.groups()
                time = datetime.strptime(time, "%I:%M %p")
                day = day.capitalize()

                days_of_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
                week_start = datetime.now() - timedelta(days=datetime.now().weekday())
                event_day = week_start + timedelta(days=days_of_week[day])

                start_time = event_day.replace(hour=time.hour, minute=time.minute)
                calendar_data[event_id]["start_time"] = start_time
            else:
                console.print("[bold red]Invalid day and time format! Please use the format: Monday 5:30 PM[/bold red]")
                return

        if duration:
            end_time = calendar_data[event_id]["start_time"] + timedelta(minutes=int(duration))
            calendar_data[event_id]["end_time"] = end_time

        calendar_data[event_id]["title"] = title
        calendar_data[event_id]["recurrence"] = recurrence

        save_calendar()
        console.print("[bold #FC6C85]Event modified successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid event ID![/bold red]")

def remove_event():
    """Remove an event from the calendar."""
    load_calendar()
    display_event_list()
    event_id = int(console.input("[#FC6C85]Enter event ID to remove: [/#FC6C85]"))
    if 0 <= event_id < len(calendar_data):
        del calendar_data[event_id]
        save_calendar()
        console.print("[bold #FC6C85]Event removed successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid event ID![/bold red]")

def display_calendar(week_start):
    """Display the weekly calendar with events."""
    load_calendar()
    table = Table(title="Weekly Calendar", show_lines=True, style="bold #FC6C85")
    
    # Create time column
    table.add_column("Time", style="#FC6C85", width=8)
    
    # Create columns for each day of the week
    days = [(week_start + timedelta(days=i)).strftime("%B %d\n%A") for i in range(7)]
    for day in days:
        table.add_column(day, style="#FC6C85", width=16)

    # Initialize empty rows for each 15-minute slot from 6 AM to 12 AM
    time_slots = [(datetime.min + timedelta(minutes=15 * i)).strftime('%I:%M %p') for i in range(6 * 4, 24 * 4)]
    rows = [[""] * 7 for _ in time_slots]

    # Create a dictionary to hold the events for each day
    day_events = {day: [] for day in days}
    for event in calendar_data:
        event_day = event["start_time"].strftime("%B %d\n%A")
        if event_day in day_events:
            day_events[event_day].append(event)

    # Sort the events for each day by their start time
    for day in day_events:
        day_events[day].sort(key=lambda e: e["start_time"])

    # Place events in the appropriate rows
    for day_idx, day in enumerate(days):
        events = day_events[day]
        for event in events:
            start_index = (event["start_time"].hour - 6) * 4 + event["start_time"].minute // 15
            duration = int((event["end_time"] - event["start_time"]).total_seconds() / 60 // 15)
            event_str = f"{event['title']}"
            for i in range(duration):
                if i == 0:
                    rows[start_index + i][day_idx] = f"[bold on #FC6C85 white]{event_str:<15}[/bold on #FC6C85 white]"
                else:
                    rows[start_index + i][day_idx] = f"[on #FC6C85]{'|':<15}[/on #FC6C85]"  # Continue the block

    # Add time slots and rows to the table
    for time_slot, row in zip(time_slots, rows):
        table.add_row(time_slot, *row)

    console.print(table)
