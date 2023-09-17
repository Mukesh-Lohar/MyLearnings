

from documentation.documentation import Document


document = Document("Sample Document", "John Doe")
document.add_heading("# Introduction")
document.add_paragraph("This is an example document.")
document.add_heading("## Section 1")
document.add_paragraph("This is section 1.")
document.add_heading("## Section 2")
document.add_paragraph("This is section 2.")
document.add_list(["Item 1", "Item 2", "Item 3"])

# Create a PDF from the document content
document.create_pdf("sample_document.pdf")
