from docx import Document
from pypdf import PdfReader


def read_txt(file):
    return file.read().decode("utf-8")


def read_docx(file):
    doc = Document(file)
    return "\n".join([p.text for p in doc.paragraphs])


def read_pdf(file):
    reader = PdfReader(file)
    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def read_file(uploaded_file):
    extension = uploaded_file.name.split(".")[-1].lower()

    if extension == "txt":
        return read_txt(uploaded_file)

    if extension == "docx":
        return read_docx(uploaded_file)

    if extension == "pdf":
        return read_pdf(uploaded_file)

    return ""