import os
import subprocess
from rich.console import Console
from rich.tree import Tree

console = Console()
notes_directory = "notes_files"  # Directory to store notes

# Ensure the notes directory exists
os.makedirs(notes_directory, exist_ok=True)

def display_folders():
    """Display all folders."""
    folders = [f for f in os.listdir(notes_directory) if os.path.isdir(os.path.join(notes_directory, f))]
    if not folders:
        console.print("[bold #FC6C85]No folders available.[/bold #FC6C85]")
        return

    console.print("[bold #FC6C85]Folders:[/bold #FC6C85]")
    for folder in folders:
        console.print(f"- {folder}")

def display_notes_tree():
    """Display all folders and notes in a tree format."""
    tree = Tree("[bold #FC6C85]Notes[/bold #FC6C85]")
    folders = [f for f in os.listdir(notes_directory) if os.path.isdir(os.path.join(notes_directory, f))]
    
    for folder in folders:
        folder_node = tree.add(f"[bold magenta]{folder}[/bold magenta]")
        folder_path = os.path.join(notes_directory, folder)
        notes = [f for f in os.listdir(folder_path) if f.endswith('.md')]
        for note in notes:
            folder_node.add(note[:-3])
    
    console.print(tree)

def new_folder():
    """Add a new folder."""
    folder = console.input("[#FC6C85]Folder name: [/#FC6C85]")
    folder_path = os.path.join(notes_directory, folder)
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        console.print(f"[bold #FC6C85]Folder '{folder}' created successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Folder already exists.[/bold red]")

def new_note():
    """Add a new note in a folder."""
    display_folders()
    folder = console.input("[#FC6C85]Enter folder name to add note to: [/#FC6C85]")
    folder_path = os.path.join(notes_directory, folder)
    if not os.path.exists(folder_path):
        console.print("[bold red]Folder not found! Please create the folder first.[/bold red]")
        return

    title = console.input("[#FC6C85]Note title: [/#FC6C85]")
    file_path = os.path.join(folder_path, f"{title}.md")

    if os.path.exists(file_path):
        console.print("[bold red]Note already exists. Opening existing note.[/bold red]")
    else:
        console.print("[bold #FC6C85]Creating new note.[/bold #FC6C85]")

    open_note_in_editor(file_path)

def open_note_in_editor(file_path):
    """Open a note in the default text editor."""
    try:
        editor = os.environ.get('EDITOR', 'nano')  # Use 'nano' editor by default
        subprocess.run([editor, file_path])
    except Exception as e:
        console.print(f"[bold red]Failed to open editor: {e}[/bold red]")

def delete_note():
    """Delete an existing note."""
    display_folders()
    folder = console.input("[#FC6C85]Enter folder name to delete note from: [/#FC6C85]")
    folder_path = os.path.join(notes_directory, folder)
    if not os.path.exists(folder_path):
        console.print("[bold red]Folder not found![/bold red]")
        return

    title = console.input("[#FC6C85]Enter note title to delete: [/#FC6C85]")
    file_path = os.path.join(folder_path, f"{title}.md")

    if os.path.exists(file_path):
        os.remove(file_path)
        console.print("[bold #FC6C85]Note deleted successfully![/bold #FC6C85]")
    else:
        console.print("[bold red]Note not found![/bold red]")

def delete_folder():
    """Delete an existing folder and its contents."""
    display_folders()
    folder = console.input("[#FC6C85]Enter folder name to delete: [/#FC6C85]")
    folder_path = os.path.join(notes_directory, folder)
    if not os.path.exists(folder_path):
        console.print("[bold red]Folder not found![/bold red]")
        return

    confirm = console.input(f"[#FC6C85]Are you sure you want to delete the folder '{folder}' and all its contents? (y/n): [/#FC6C85]").strip().lower()
    if confirm == 'y':
        for root, dirs, files in os.walk(folder_path, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(folder_path)
        console.print("[bold #FC6C85]Folder deleted successfully![/bold #FC6C85]")
    else:
        console.print("[bold #FC6C85]Folder deletion canceled.[/bold #FC6C85]")
