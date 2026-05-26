from fastapi import FastAPI



app = FastAPI()

@app.get("/",tags=["Agent-Safe"])
async def root():
    return {"message": "FastAPI is running!"}


@app.get("/notes",tags=["Agent-Safe"])
async def get_notes():
    return {"message": "This will return all notes."}

@app.post("/notes",tags=["Agent-Safe"])
async def create_note():
    return {"message": "This will create a new note."}

@app.get("/notes/{note_id}",tags=["Agent-Safe"])
async def get_note(note_id: str):
    return {"message": f"This will return note with id {note_id}."}

@app.put("/notes/{note_id}",tags=["Agent-Safe"])
async def update_note(note_id: str):
    return {"message": f"This will update note with id {note_id}."}

@app.delete("/notes/{note_id}",tags=["Agent-restricted"])
async def delete_note(note_id: str):
    return {"message": f"This will delete note with id {note_id}."}

