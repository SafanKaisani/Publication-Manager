from fpdf import FPDF

def export_publications_to_pdf(publications, filename="publications.pdf"):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Publications List", ln=True, align='C')
    pdf.ln(10)
    for pub in publications:
        pdf.cell(0, 10, txt=f"Title: {pub.title} | Year: {pub.year} | Authors: {', '.join([a.author.name for a in pub.authors])}", ln=True)
    pdf.output(filename)

# Example usage:

class Author:
    def __init__(self, name):
        self.name = name

class AuthorRole:
    def __init__(self, author):
        self.author = author

class Publication:
    def __init__(self, title, year, authors):
        self.title = title
        self.year = year
        self.authors = authors

if __name__ == "__main__":
    publications = [
        Publication("Deep Learning for Cats", "2022", [AuthorRole(Author("Alice")), AuthorRole(Author("Bob"))]),
        Publication("AI in Healthcare", "2023", [AuthorRole(Author("Carol"))])
    ]
    export_publications_to_pdf(publications, "test_publications.pdf")