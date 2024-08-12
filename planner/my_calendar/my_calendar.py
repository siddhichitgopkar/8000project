from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
import re
from calendar_utils import load_calendar, save_calendar, calendar_data

console = Console()

def display_calendar(week_start):
    load_calendar()  # Load calendar data each time you display the calendar
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
                    block = f"[bold white on #D2042D]{event['title']}[/bold white on #D2042D]"
                    break
            row.append(block)
        table.add_row(*row)
    
    console.print(table)

def display_event_list():
    load_calendar()  # Load calendar data each time you display the event list
    for i, event in enumerate(calendar_data):
        console.print(f"[{i}] {event['title']} on {event['start_time'].strftime('%A %I:%M %p')} to {event['end_time'].strftime('%I:%M %p')}")

def add_event():
    load_calendar()  # Load calendar data before adding an event
    title = console.input("[#FC6C85]Event title: [/#FC6C85]")
    day_time = console.input("[#FC6C85]Enter day and time (e.g., Monday 5:30 PM): [/#FC6C85]")
    duration = int(console.input("[#FC6C85]Enter event duration in minutes: [/#FC6C85]"))
    recurrence = console.input("[#FC6C85]Recurrence (none, daily, weekly, monthly) (default: none): [/#FC6C85]") or "none"
    recurrence_weeks = int(console.input("[#FC6C85]Number of weeks to recur (default: 4): [/#FC6C85]") or 4)

    match = re.match(r"(\w+)\s+(\d{1,2}:\d{2}\s*[APMapm]{2})", day_time)
    if match:
        day, time = match.groups()
        time = datetime.strptime(time, "%I:%M %p")
        day = day.capitalize()

        days_of_week = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
        week_start = datetime.now() - timedelta(days=datetime.now().weekday())
        event_day = week_start + timedelta(days=days_of_week[day])

        start_time = event_day.replace(hour=time.hour, minute=time.minute)
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
                next_month = (start_time.month % 12) + 1
                start_time = start_time.replace(month=next_month)
                end_time = end_time.replace(month=next_month)
            else:
                break

        save_calendar()  # Save calendar data after adding an event
        console.print("[bold #FC6C85]Event added successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid day and time format! Please use the format: Monday 5:30 PM[/bold red]")

def modify_event():
    load_calendar()  # Load calendar data before modifying an event
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

                if duration:
                    end_time = start_time + timedelta(minutes=int(duration))
                    calendar_data[event_id]["end_time"] = end_time

        calendar_data[event_id]["title"] = title
        calendar_data[event_id]["recurrence"] = recurrence

        save_calendar()  # Save calendar data after modifying an event
        console.print("[bold #FC6C85]Event modified successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid event ID![/bold red]")

def remove_event():
    load_calendar()  # Load calendar data before removing an event
    display_event_list()
    event_id = int(console.input("[#FC6C85]Enter event ID to remove: [/#FC6C85]"))
    if 0 <= event_id < len(calendar_data):
        del calendar_data[event_id]
        save_calendar()  # Save calendar data after removing an event
        console.print("[bold #FC6C85]Event removed successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Invalid event ID![/bold red]")
