import fitz 

def extract_text(file_type: str, content_bytes: bytes) -> str:
    """
    Extract text from .txt or .pdf content bytes.

    Args:
        file_type (str): MIME type of the file ('text/plain' or 'application/pdf').
        content_bytes (bytes): The raw content of the file.

    Returns:
        str: Extracted text content.

    Raises:
        ValueError: If the file type is unsupported or content is empty/unreadable.
        RuntimeError: If reading a PDF fails.
    """
    content = ""

    if file_type == 'text/plain':
        content = content_bytes.decode('utf-8')
    elif file_type == 'application/pdf':
        try:
            with fitz.open(stream=content_bytes, filetype="pdf") as doc:
                for page in doc:
                    content += page.get_text()
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF: {e}") from e
    else:
        raise ValueError("Unsupported file type. Please upload .txt or .pdf")

    if not content.strip():
        raise ValueError("The file appears to be empty or unreadable.")
    
    return content