from documentation.schemas import (DocumentElement,
                                   HeaderFooter,
                                   Heading,
                                   TableOfContents)

from dataclasses import dataclass, field
import PyPDF2


@dataclass
class Document:
    title: str
    author: str
    content: list[DocumentElement] = field(default_factory=list)
    metadata: dict = field(default_factory=dict)
    page_numbering: str = "arabic"
    headers: HeaderFooter = field(default_factory=lambda: HeaderFooter("Header Text",
                                                                       "center"))
    footers: HeaderFooter = field(default_factory=lambda: HeaderFooter("Footer Text",
                                                                       "center"))
    table_of_contents: TableOfContents = field(default_factory=lambda: TableOfContents()) ## noqa:E501
    language: str = "en"

    def add_element(self, element: DocumentElement):
        self.content.append(element)

    def generate_toc(self):
        # Generate the Table of Contents based on headings in the document
        self.table_of_contents.headings.clear()  # Clear existing TOC
        headings_stack = []  # Stack to track nested headings and their level
        for element in self.content:
            if isinstance(element, Heading):
                while headings_stack and headings_stack[-1].level >= element.level:
                    headings_stack.pop()
                self.table_of_contents.headings.append(element)
                headings_stack.append(element)

    def create_pdf(self, filename):
        PyPDF2.PdfFileWriter()

        # Create a PDF page for each content item (heading, paragraph, list)
