# ruff: noqa: E501


from dataclasses import dataclass, field

@dataclass
class FontStyle:
    font_name: str = "Times New Roman"
    font_size: int = 10
    font_bold: bool = False
    font_italic: bool = False
    font_color: str = "#000000"  # Default to black

@dataclass
class DocumentElement:
    title: str
    content: str = ""
    font_style: FontStyle = field(default_factory=lambda: FontStyle())
    bullet_point: bool = False
    numbering: bool = False

@dataclass
class Image(DocumentElement):
    path: str = "image.png"
    width: int = 0
    height: int = 0

@dataclass
class Heading(DocumentElement):
    level: int = 1
    font_style: FontStyle = field(default_factory=lambda: FontStyle(font_bold=True))  # Bold by default
    paragraphs: list['Paragraph'] = field(default_factory=list)  # list of linked paragraphs
    subheadings: list['Heading'] = field(default_factory=list)  # list of nested subheadings

@dataclass
class Paragraph(DocumentElement):
    alignment: str = "left"
    line_spacing: float = 1.0
    indentation: int = 0
    image : Image | None = None


@dataclass
class Quote(DocumentElement):
    pass

@dataclass
class CodeBlock(DocumentElement):
    language: str = "python"

@dataclass
class Equation(DocumentElement):
    pass

@dataclass
class Annotation(DocumentElement):
    pass

@dataclass
class Reference(DocumentElement):
    pass

@dataclass
class Footnote(DocumentElement):
    pass

@dataclass
class PageBreak(DocumentElement):
    pass

@dataclass
class Watermark(DocumentElement):
    pass

@dataclass
class HeaderFooter:
    content: str = ""
    alignment: str = "center"
    font_style: FontStyle = field(default_factory=lambda: FontStyle())


@dataclass
class Table(DocumentElement):
    rows: list[list[str]] = field(default_factory=list)
    column_headers: list[str] = field(default_factory=list)

@dataclass
class TableOfContents:
    headings: list[Heading] = field(default_factory=list)
    tables: list['Table'] = field(default_factory=list)
    figures: list['Figure'] = field(default_factory=list)

@dataclass
class Figure(DocumentElement):
    caption: str = ""




@dataclass
class DocumentModel:
    title: str
    author: str
    content: list[DocumentElement] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    page_numbering: str = "arabic"
    headers: HeaderFooter = field(default_factory=lambda: HeaderFooter("Header Text", "center"))
    footers: HeaderFooter = field(default_factory=lambda: HeaderFooter("Footer Text", "center"))
    table_of_contents: TableOfContents = field(default_factory=lambda: TableOfContents())
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


    def _get_toc_content(self, headings, n=0, headings_stack_dict={}):

        headings_stack_dict[n] = (headings.level, headings.title)

        if headings.subheadings:
            for subheading in heading.subheadings:
                self._get_toc_content(subheading, n + 1, headings_stack_dict)

        return headings_stack_dict

    def generate_toc(self):
        if not self.content:
            return print("no content")
        # Initialize a dictionary to store the TOC content

        toc_content =[]
        for heading in self.content:
            if isinstance(heading,Heading):
                toc_content.append(self._get_toc_content(heading))

        # Generate the Table of Contents based on the collected headings
        self.table_of_contents.headings.clear()  # Clear existing TOC
        print(toc_content)
        for block in toc_content:
            for k,v in block.items():
                indent = "    " * v[0]  # Adjust the indentation based on the heading level

                title = f"{indent}{v[1]}"  # Create a TOC entry
                remaining_chars = self.max_lenth - len(title)
                title += "-"*remaining_chars
                print(title)
                self.table_of_contents.headings.append(block)

        return self.table_of_contents
# Example usage:
document = DocumentModel("Sample Document", "John Doe")
# Add headings and content to the document
# ...
subheadings = Heading(title="subheading",level=2)
heading = Heading(title= "main heading", subheadings=[subheadings])
heading2 = Heading(title= "main heading2", subheadings=[subheadings])

document.add_element(heading)
document.add_element(heading2)

# Generate the Table of Contents
(f"{document.generate_toc()}")