import fitz 

def extract_text(file_type, content_bytes):
    """
    Extract text from .txt or .pdf content bytes.
    Returns:
      Extracted text (str).
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
            raise Exception(f"Failed to read PDF: {e}") from e
    else:
        raise Exception("Unsupported file type. Please upload .txt or .pdf")

    if not content or not content.strip():
        raise Exception("The file appears to be empty or unreadable.")
    
    return content