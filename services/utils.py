# services/utils.py
import re

def validate_query(query):
    """Validate a natural language query for safety and basic sanity."""
    if not query or not query.strip():
        return False
    
    # Check for SQL-like patterns in the natural language input
    sql_patterns = [
        r'\bSELECT\b', r'\bINSERT\b', r'\bUPDATE\b', r'\bDELETE\b',
        r'\bDROP\b', r'\bTRUNCATE\b', r';', r'--', r'/\*'
    ]
    if any(re.search(pattern, query, re.IGNORECASE) for pattern in sql_patterns):
        return False
    
    # Basic length check
    if len(query.strip()) < 3 or len(query.strip()) > 500:
        return False
    
    return True

def sanitize_input(text):
    """Sanitize input by removing potentially harmful characters."""
    return re.sub(r'[;`\'"]', '', text).strip()