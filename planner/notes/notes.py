import os
import subprocess
from rich.console import Console

console = Console()
notes_directory = "notes_files"  # Directory to store notes

# Ensure the notes directory exists
os.makedirs(notes_directory, exist_ok=True)

def display_notes():
    """Display all notes."""
    notes = [f for f in os.listdir(notes_directory) if f.endswith('.txt')]
    if not notes:
        console.print("[bold #FC6C85]No notes available.[/bold #FC6C85]")
        return

    console.print("[bold #FC6C85]Notes:[/bold #FC6C85]")
    for note in notes:
        console.print(f"- {note[:-4]}")

def add_note():
    """Add a new note."""
    title = console.input("[#FC6C85]Note title: [/#FC6C85]")
    file_path = os.path.join(notes_directory, f"{title}.txt")

    if os.path.exists(file_path):
        console.print("[bold red]Note already exists. Opening existing note.[/bold red]")
    else:
        console.print("[bold #FC6C85]Creating new note.[/bold #FC6C85]")

    open_note_in_editor(file_path)

def modify_note():
    """Modify an existing note."""
    display_notes()
    title = console.input("[#FC6C85]Enter note title to modify: [/#FC6C85]")
    file_path = os.path.join(notes_directory, f"{title}.txt")

    if os.path.exists(file_path):
        console.print("[bold #FC6C85]Opening note for editing.[/bold #FC6C85]")
        open_note_in_editor(file_path)
    else:
        console.print("[bold red]Note not found![/bold red]")

def open_note_in_editor(file_path):
    """Open a note in the default text editor."""
    try:
        editor = os.environ.get('EDITOR', 'nano')  # Use 'nano' editor by default
        subprocess.run([editor, file_path])
    except Exception as e:
        console.print(f"[bold red]Failed to open editor: {e}[/bold red]")
