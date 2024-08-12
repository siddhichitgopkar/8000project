import json
import os
from datetime import datetime

calendar_data = []
calendar_file = "calendar_data.json"

def load_calendar():
    global calendar_data
    if os.path.exists(calendar_file):
        with open(calendar_file, 'r') as f:
            try:
                calendar_data = json.load(f)
                for event in calendar_data:
                    event["start_time"] = datetime.strptime(event["start_time"], "%Y-%m-%d %H:%M:%S.%f")
                    event["end_time"] = datetime.strptime(event["end_time"], "%Y-%m-%d %H:%M:%S.%f")
            except json.JSONDecodeError:
                calendar_data = []
            except ValueError:
                calendar_data = []
    else:
        calendar_data = []

def save_calendar():
    with open(calendar_file, 'w') as f:
        json.dump(calendar_data, f, default=str)

def add_event_at_time(title, start_time, end_time):
    load_calendar()  # Make sure we are working with the latest data
    calendar_data.append({
        "title": title,
        "start_time": start_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "end_time": end_time.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "recurrence": "none"
    })
    save_calendar()
