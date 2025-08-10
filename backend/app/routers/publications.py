from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
from .. import models, schemas, crud
from ..database import get_db
from ..auth import get_current_user
import uuid
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=schemas.PublicationRead)
def create_publication(publication: schemas.PublicationCreate, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    try:
        return crud.create_publication(db=db, publication=publication)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[schemas.PublicationRead])
def read_publications(skip: int = 0, limit: int = 100, author: str = None, topic: str = None, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    publications = crud.get_publications(db, skip=skip, limit=limit, author=author, topic=topic)
    if not publications:
        raise HTTPException(status_code=404, detail="No publications found")
    return publications

@router.get("/pdf")
def get_publications_pdf(author: str = None, topic: str = None, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    publications = crud.get_publications(db, author=author, topic=topic)
    if not publications:
        raise HTTPException(status_code=404, detail="No publications found for the given filters")
    unique_id = uuid.uuid4().hex
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"publications_{timestamp}_{unique_id}.pdf"
    export_publications_to_pdf(publications, filename)
    return FileResponse(filename, media_type="application/pdf", filename=filename)

@router.delete("/{publication_id}", status_code=204)
def delete_publication(publication_id: int, db: Session = Depends(get_db), user: models.User = Depends(get_current_user)):
    if not crud.delete_publication(db, publication_id):
        raise HTTPException(status_code=404, detail=f"Publication with ID {publication_id} not found")