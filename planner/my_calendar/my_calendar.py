import json
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
import re

console = Console()
calendar_data = []
calendar_file = "calendar_data.json"

def load_calendar():
    global calendar_data
    if os.path.exists(calendar_file):
        with open(calendar_file, 'r') as f:
            calendar_data = json.load(f)
            for event in calendar_data:
                event["start_time"] = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M:%S.%f")
                event["end_time"] = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M:%S.%f")

def save_calendar():
    with open(calendar_file, 'w') as f:
        json.dump(calendar_data, f, default=str)

def display_calendar(week_start):
    load_calendar()
    table = Table(title="Weekly Calendar", show_lines=True, style="bold #FC6C85")
    table.add_column("Time", style="#FC6C85", width=10)
    days = [(week_start + timedelta(days=i)).strftime("%B %d\n%A") for i in range(7)]
    for day in days:
        table.add_column(day, style="#FC6C85", width=20)
    
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
                    block = f"[bold #FC6C85]{event['title']}[/bold #FC6C85]"
                    break
            row.append(block)
        table.add_row(*row)
    
    console.print(table)

def display_event_list():
    load_calendar()
    for i, event in enumerate(calendar_data):
        console.print(f"[{i}] {event['title']} on {event['start_time'].strftime('%A %I:%M %p')} to {event['end_time'].strftime('%I:%M %p')}")

def add_event():
    load_calendar()
    title = console.input("[#FC6C85]Event title: [/#FC6C85]")
    day_time = console.input("[#FC6C85]Enter day and time (e.g., Monday 5:30 PM): [/#FC6C85]")
    duration = int(console.input("[#FC6C85]Enter event duration in hours: [/#FC6C85]"))
    recurrence = console.input("[#FC6C85]Recurrence (none, daily, weekly, monthly) (default: none): [/#FC6C85]") or "none"

    match = re.match(r"(\w+)\s+(\d{1,2}:\d{2}\s*[APMapm]{2})", day_time)
    if match:
        day, time = match.groups()
        time = datetime.strptime(time, "%I:%M %p")
        day = day.capitalize()

        days_of_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        event_day = week_start + timedelta(days=days_of_week[day])

        start_time = event_day.replace(hour=time.hour, minute=time.minute)
        end_time = start_time + timedelta(hours=duration)
        
        calendar_data.append({"title": title, "start_time": start_time, "end_time": end_time, "recurrence": recurrence})
        save_calendar()
        console.print("[bold #FC6C85]Event added successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid day and time format! Please use the format: Monday 5:30 PM[/bold red]")

def modify_event():
    load_calendar()
    display_event_list()
    event_id = int(console.input("[#FC6C85]Enter event ID to modify: [/#FC6C85]"))
    if 0 <= event_id < len(calendar_data):
        title = console.input("[#FC6C85]New event title: [/#FC6C85]") or calendar_data[event_id]["title"]
        day_time = console.input("[#FC6C85]New day and time (e.g., Monday 5:30 PM): [/#FC6C85]")
        duration = console.input("[#FC6C85]New event duration in hours: [/#FC6C85]")
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
            end_time = calendar_data[event_id]["start_time"] + timedelta(hours=int(duration))
            calendar_data[event_id]["end_time"] = end_time

        calendar_data[event_id]["title"] = title
        calendar_data[event_id]["recurrence"] = recurrence

        save_calendar()
        console.print("[bold #FC6C85]Event modified successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid event ID![/bold red]")

def remove_event():
    load_calendar()
    display_event_list()
    event_id = int(console.input("[#FC6C85]Enter event ID to remove: [/#FC6C85]"))
    if 0 <= event_id < len(calendar_data):
        del calendar_data[event_id]
        save_calendar()
        console.print("[bold #FC6C85]Event removed successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid event ID![/bold red]")

def add_event_at_time(title, start_time, end_time):
    load_calendar()
    calendar_data.append({"title": title, "start_time": start_time, "end_time": end_time, "recurrence": "none"})
    save_calendar()
