from fastapi import FastAPI, HTTPException, Depends
from starlette import status
from config.models import NoteCreateRequest, NoteEditRequest, Note
from sqlalchemy.ext.asyncio import AsyncSession
from config.db import get_db
from sqlalchemy import select
from typing import Annotated
from fastapi_mcp import FastApiMCP


app = FastAPI()

dependency = Annotated[AsyncSession, Depends(get_db)]


@app.get("/", tags=["Agent-Safe"])
async def root():
    return {"message": "FastAPI is running!"}


@app.get("/notes", tags=["Agent-Safe"], status_code=status.HTTP_200_OK)
async def get_notes(db: dependency):
    notes = await db.execute(select(Note))
    data = notes.scalars().all()
    if not data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No notes found")
    return {"message": "notes fetched successfully", "success": True, "data": data}


@app.post("/notes", tags=["Agent-Safe"], status_code=status.HTTP_201_CREATED)
async def create_note(db: dependency, note_request: NoteCreateRequest):
    note = Note(**note_request.dict())
    if not note:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid note data")
    db.add(note)
    await db.commit()
    await db.refresh(note)
    return {"message": "New note created successfully", "success": True, "data": note}


@app.get("/notes/{note_id}", tags=["Agent-Safe"], status_code=status.HTTP_200_OK)
async def get_note(note_id: str, db: dependency):
    note = await db.execute(select(Note).where(Note.id == note_id))
    data = note.scalar_one_or_none()  # not awaited
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No note found with id {note_id}")
    return {"message": f"Note with id {note_id} fetched successfully", "success": True, "data": data}


@app.put("/notes/{note_id}", tags=["Agent-Safe"], status_code=status.HTTP_200_OK)
async def update_note(note_id: str, db: dependency, note_request: NoteEditRequest):
    note = await db.execute(select(Note).where(Note.id == note_id))
    data = note.scalar_one_or_none()  # not awaited; `detail` not `details`
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No note found with id {note_id}")

    data.title = note_request.title
    data.description = note_request.description
    data.tags = note_request.tags

    await db.commit()
    await db.refresh(data)
    return {"message": f"Note with id {note_id} updated successfully", "success": True, "data": data}


@app.delete("/notes/{note_id}", tags=["Agent-restricted"], status_code=status.HTTP_200_OK)
async def delete_note(note_id: str, db: dependency):
    note = await db.execute(select(Note).where(Note.id == note_id))
    data = note.scalar_one_or_none()  # not awaited; `detail` not `details`
    if data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No note found with id {note_id}")

    await db.delete(data)
    await db.commit()
    return {"message": f"Note with id {note_id} deleted successfully", "success": True, "data": data}


mcp = FastApiMCP(app, include_tags=["Agent-Safe"], exclude_tags=["Agent-restricted"])
mcp.mount()