import json
import os
from datetime import datetime

# Global variables
calendar_data = []
calendar_file = "calendar_data.json"

def load_calendar():
    """Load calendar data from a JSON file."""
    global calendar_data
    if os.path.exists(calendar_file):
        with open(calendar_file, 'r') as f:
            try:
                calendar_data = json.load(f)
                for event in calendar_data:
                    try:
                        # Try to parse datetime with microseconds
                        event["start_time"] = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M:%S.%f")
                        event["end_time"] = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        # Fallback to parsing without microseconds
                        event["start_time"] = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M:%S")
                        event["end_time"] = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M:%S")
            except (json.JSONDecodeError, ValueError) as e:
                print(f"Error loading calendar data: {e}")
                calendar_data = []
    else:
        calendar_data = []

def save_calendar():
    """Save calendar data to a JSON file."""
    data_to_save = []
    for event in calendar_data:
        data_to_save.append({
            "title": event["title"],
            "start_time": event["start_time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
            "end_time": event["end_time"].strftime("%Y-%m-%d %H:%M:%S.%f"),
            "recurrence": event["recurrence"]
        })

    try:
        with open(calendar_file, 'w') as f:
            json.dump(data_to_save, f, default=str)
    except IOError as e:
        print(f"Error saving calendar data: {e}")

def add_event_at_time(title, start_time, end_time):
    """Add a new event to the calendar."""
    load_calendar()  # Ensure we're working with the latest data
    calendar_data.append({
        "title": title,
        "start_time": start_time,
        "end_time": end_time,
        "recurrence": "none"
    })
    save_calendar()
