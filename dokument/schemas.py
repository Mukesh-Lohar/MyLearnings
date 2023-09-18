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
    font_style: FontStyle = field(
        default_factory=lambda: FontStyle(font_bold=True),
    )  # Bold by default
    paragraphs: list["Paragraph"] = field(
        default_factory=list,
    )  # list of linked paragraphs
    subheadings: list["Heading"] = field(
        default_factory=list,
    )  # list of nested subheadings


@dataclass
class Paragraph(DocumentElement):
    alignment: str = "left"
    line_spacing: float = 1.0
    indentation: int = 0
    image: Image | None = None


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
    tables: list["Table"] = field(default_factory=list)
    figures: list["Figure"] = field(default_factory=list)


@dataclass
class Figure(DocumentElement):
    caption: str = ""
