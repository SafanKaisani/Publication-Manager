import pandas as pd
from .database import SessionLocal
from . import crud, schemas

def import_publications_from_excel(file_path: str):
    df = pd.read_excel(file_path)
    db = SessionLocal()
    for _, row in df.iterrows():
        # Parse authors from Excel (assume comma-separated names and roles)
        authors = []
        if 'Authors' in row and pd.notna(row['Authors']):
            author_entries = str(row['Authors']).split(';')
            for entry in author_entries:
                # Example format: "John Doe (Lead); Jane Smith (Co-author)"
                if '(' in entry and ')' in entry:
                    name, role = entry.split('(')
                    role = role.replace(')', '').strip()
                    name = name.strip()
                else:
                    name = entry.strip()
                    role = None
                authors.append(
                    schemas.AuthorRoleCreate(
                        role=role,
                        author=schemas.AuthorCreate(name=name)
                    )
                )

        pub_data = schemas.PublicationCreate(
            entry_date=row.get('Entry Date', None),
            publication_type=row.get('Type', None),
            year=str(row.get('Year', '')),
            title=row['Title'],
            status=row.get('Status', None),
            reference=row.get('Reference', ''),
            theme=row.get('Theme', ''),
            authors=authors
        )
        crud.create_publication(db, publication=pub_data)
    db.close()

# To run the import directly:
if __name__ == "__main__":
    import_publications_from_excel("D:\\Publication_Manager\\Publication details.xlsx")