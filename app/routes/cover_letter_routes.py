from typing import List
from fastapi import APIRouter, HTTPException, Path, Body
from app.models.cover_letter_model import CoverLetter, CoverLetterCreate, CoverLetterUpdate
from app.services.cover_letter_service import CoverLetterService

router = APIRouter()
cover_letter_service = CoverLetterService()

@router.post("/", response_model=CoverLetter, status_code=201)
async def create_cover_letter(cover_letter_data: CoverLetterCreate):
    """
    Create a new cover letter.
    """
    # Construct CoverLetterData
    content_data = cover_letter_data.model_dump(exclude={'resume_id', 'job_profile_id'})
    
    # Construct CoverLetter Document
    cover_letter = CoverLetter(
        content=content_data, # Pydantic will validate this against CoverLetterData
        resume_id=cover_letter_data.resume_id,
        job_profile_id=cover_letter_data.job_profile_id
    )
    return await cover_letter_service.create_cover_letter(cover_letter)

@router.get("/", response_model=List[CoverLetter])
async def get_all_cover_letters():
    """
    Get all cover letters.
    """
    return await cover_letter_service.get_all_cover_letters()

@router.get("/{id}", response_model=CoverLetter)
async def get_cover_letter(id: str = Path(..., title="The ID of the cover letter to get")):
    """
    Get a specific cover letter by ID.
    """
    cover_letter = await cover_letter_service.get_cover_letter(id)
    if not cover_letter:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    return cover_letter

@router.patch("/{id}", response_model=CoverLetter)
async def update_cover_letter(
    id: str = Path(..., title="The ID of the cover letter to update"),
    updates: CoverLetterUpdate = Body(...)
):
    """
    Update a cover letter.
    """
    update_data = updates.model_dump(exclude_unset=True)
    
    # Separation of concerns: We need to map flat updates to the nested structure
    # For MongoDB, we can use dot notation for nested fields, but typically repository handles that.
    # However, our repository implementation (generic) takes a dict and calls .set().
    # So we should prepare the dict with dot notation for nested fields or structure modification.
    
    # Actually, Beanie's .set() accepts a dictionary. If we pass {"content.title": "New Title"}, it works?
    # Or should we reconstruct the object?
    # Let's try to map the top-level keys that belong to content to "content.KEY"
    
    final_updates = {}
    content_fields = [
        "title", "client_name", "hiring_manager", "job_details", 
        "word_count", "opening_paragraph", "body_paragraphs", 
        "company_connection", "closing_paragraph"
    ]
    
    for key, value in update_data.items():
        if key in content_fields:
            # Need to handle alias if they differ in the Data model? 
            # CoverLetterData uses aliases like "clientName" for "client_name".
            # Beanie/Pydantic might expect the python attribute name if using .set({ "content.client_name": ... })
            # or the aliased name? Beanie usually works with python attribute names.
            # CoverLetterData has python attributes like client_name.
            final_updates[f"content.{key}"] = value
        elif key in ["resume_id", "job_profile_id"]:
            final_updates[key] = value
            
    cover_letter = await cover_letter_service.update_cover_letter(id, final_updates)
    if not cover_letter:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    return cover_letter

@router.delete("/{id}", response_model=bool)
async def delete_cover_letter(id: str = Path(..., title="The ID of the cover letter to delete")):
    """
    Delete a cover letter.
    """
    deleted = await cover_letter_service.delete_cover_letter(id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Cover letter not found")
    return True
