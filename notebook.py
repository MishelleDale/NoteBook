import json
import os
from datetime import datetime

class Note:
    def __init__(self, title, body):
        self.title = title
        self.body = body
        self.creation_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def __str__(self):
        return f"{self.title}\n{self.body}\n{self.creation_date}\n"
    
class NoteBook:
    def __init__(self, notes_filename="notes.json"):
        self.notes_filename = notes_filename
        self.notes = self.load_notes()
    
    def load_notes(self):
        if os.path.exists(self.notes_filename):
            with open(self.notes_filename, "r") as f:
                notes = json.load(f)
                return {int(id): Note(note["title"], note["body"]) for id, note in notes.items()}
        else:
            return {}
    
    def save_notes(self):
        with open(self.notes_filename, "w") as f:
            notes_dict = {id: {"title": note.title, "body": note.body} for id, note in self.notes.items()}
            json.dump(notes_dict, f)
    
    def create_note(self):
        title = input("Enter note title: ")
        body = input("Enter note body: ")
        note = Note(title, body)
        new_id = max(self.notes.keys(), default=0) + 1
        self.notes[new_id] = note
        self.save_notes()
    
    def read_notes(self):
        if not self.notes:
            print("There are no notes to display.")
            return
        for id, note in self.notes.items():
            print(f"Note ID: {id}\n{note}")
    
    def edit_note(self):
        note_id = int(input("Enter note ID to edit: "))
        if note_id not in self.notes:
            print("Invalid note ID")
            return
        title = input("Enter new title (press enter to skip): ")
        body = input("Enter new body (press enter to skip): ")
        note = self.notes[note_id]
        if title:
            note.title = title
        if body:
            note.body = body
        self.save_notes()
    
    def delete_note(self):
        note_id = int(input("Enter note ID to delete: "))
        if note_id not in self.notes:
            print("Invalid note ID")
            return
        del self.notes[note_id]
        self.save_notes()

if __name__ == "__main__":
    notebook = NoteBook()
    
    while True:
        command = input("Enter a command (create/read/edit/delete/quit): ")
        if command == "create":
            notebook.create_note()
        elif command == "read":
            notebook.read_notes()
        elif command == "edit":
            notebook.edit_note()
        elif command == "delete":
            notebook.delete_note()
        elif command == "quit":
            break
        else:
            print("Invalid command")
