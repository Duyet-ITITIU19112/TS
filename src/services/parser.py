from io import BytesIO
from docx import Document

def parse_file_content(filename: str, file_bytes: bytes) -> str:
    """
    Parses content from .txt or .docx files into plain text.

    Args:
        filename (str): The file's name (used to infer type).
        file_bytes (bytes): Raw bytes of the file content.

    Returns:
        str: Extracted plain text.
    """
    if filename.endswith(".txt"):
        return file_bytes.decode("utf-8", errors="ignore")

    elif filename.endswith(".docx"):
        try:
            doc = Document(BytesIO(file_bytes))
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            return f"[Error reading .docx]: {e}"

    else:
        return ""
