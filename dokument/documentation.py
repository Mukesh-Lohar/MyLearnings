from dataclasses import dataclass, field

from dokument.schemas import DocumentElement, HeaderFooter, Heading, TableOfContents


@dataclass
class DocumentModel:
    title: str
    author: str
    content: list[DocumentElement] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    page_numbering: str = "arabic"
    headers: HeaderFooter = field(
        default_factory=lambda: HeaderFooter("Header Text", "center"),
    )
    footers: HeaderFooter = field(
        default_factory=lambda: HeaderFooter("Footer Text", "center"),
    )
    table_of_contents: TableOfContents = field(
        default_factory=lambda: TableOfContents(),
    )  # E501
    language: str = "en"
    max_lenth: int = 50

    def add_element(self, element: DocumentElement):
        self.content.append(element)

    def add_heading(self, text):
        self.content.append({"type": "heading", "text": text})

    def add_paragraph(self, text):
        self.content.append({"type": "paragraph", "text": text})

    def add_list(self, items):
        self.content.append({"type": "list", "items": items})

    def _get_toc_content(self, headings, n=0, headings_stack_dict=None):
        if headings_stack_dict is None:
            headings_stack_dict = {}
        headings_stack_dict[n] = (headings.level, headings.title)

        if headings.subheadings:
            for subheading in heading.subheadings:
                self._get_toc_content(subheading, n + 1, headings_stack_dict)

        return headings_stack_dict

    def generate_toc(self):
        if not self.content:
            return "no content"
        # Initialize a dictionary to store the TOC content

        toc_content = []
        for heading in self.content:
            if isinstance(heading, Heading):
                toc_content.append(self._get_toc_content(heading))

        # Generate the Table of Contents based on the collected headings
        self.table_of_contents.headings.clear()  # Clear existing TOC
        for block in toc_content:
            for _k, v in block.items():
                indent = "    " * v[0]
                title = f"{indent}{v[1]}"  # Create a TOC entry
                remaining_chars = self.max_lenth - len(title)
                title += "-" * remaining_chars
                self.table_of_contents.headings.append(block)
        return self.table_of_contents


# Example usage:
document = DocumentModel("Sample Document", "John Doe")
# Add headings and content to the document
# ...
subheadings = Heading(title="subheading", level=2)
heading = Heading(title="main heading", subheadings=[subheadings])
heading2 = Heading(title="main heading2", subheadings=[subheadings])

document.add_element(heading)
document.add_element(heading2)

# Generate the Table of Contents
(f"{document.generate_toc()}")
