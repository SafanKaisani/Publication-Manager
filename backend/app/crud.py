# backend/app/crud.py
from sqlalchemy.orm import Session
from . import models, schemas

# ---------- CREATE ----------
def create_publication(db: Session, publication: schemas.PublicationCreate):
    # Create Publication object
    db_pub = models.Publication(
        entry_date=publication.entry_date,
        publication_type=publication.publication_type,
        year=publication.year,
        title=publication.title,
        status=publication.status,
        reference=publication.reference,
        theme=publication.theme
    )
    db.add(db_pub)
    db.flush()  # Get db_pub.id before committing

    # Add authors if provided
    if publication.authors:
        for author_role in publication.authors:
            # Check if author already exists (by name & affiliation)
            db_author = db.query(models.Author).filter(
                models.Author.name == author_role.author.name,
                models.Author.affiliation == author_role.author.affiliation
            ).first()
            if not db_author:
                db_author = models.Author(
                    name=author_role.author.name,
                    affiliation=author_role.author.affiliation
                )
                db.add(db_author)
                db.flush()

            # Link author to publication with role
            db_author_role = models.AuthorRole(
                role=author_role.role,
                publication_id=db_pub.id,
                author_id=db_author.id
            )
            db.add(db_author_role)

    db.commit()
    db.refresh(db_pub)
    return db_pub


# ---------- READ ----------
def get_publications(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Publication).offset(skip).limit(limit).all()


def get_publication(db: Session, publication_id: int):
    return db.query(models.Publication).filter(models.Publication.id == publication_id).first()


# ---------- DELETE ----------
def delete_publication(db: Session, publication_id: int):
    db_pub = db.query(models.Publication).filter(models.Publication.id == publication_id).first()
    if db_pub:
        db.delete(db_pub)
        db.commit()
        return True
    return False

# ---------- LIST BY AUTHOR ----------
def get_publications(db, skip=0, limit=100, author=None, topic=None):
    query = db.query(models.Publication)
    if author:
        query = query.join(models.Publication.authors).join(models.AuthorRole.author).filter(models.Author.name.ilike(f"%{author}%"))
    if topic:
        query = query.filter(models.Publication.theme.ilike(f"%{topic}%"))
    return query.offset(skip).limit(limit).all()