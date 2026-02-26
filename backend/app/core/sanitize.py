import re


def sanitize_text(text: str | None) -> str | None:
    """
    Sanitize text to prevent XSS.
    Strips leading/trailing whitespace, replaces > and < with HTML entities,
    and collapses multiple whitespaces into a single one.
    """
    if text is None:
        return None
    
    # Strip whitespace
    text = text.strip()
    
    # Replace < and >
    text = text.replace("<", "&lt;").replace(">", "&gt;")
    
    # Collapse multiple whitespaces
    text = re.sub(r"\s+", " ", text)
    
    return text
