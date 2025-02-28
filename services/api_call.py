import re
from groq import Groq
from config import Config

client = Groq(api_key= Config.OPENAI_API_KEY)

def call_llm(query):
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {'role': 'user', 'content': query}
            ],
            model = "deepseek-r1-distill-llama-70b"
        )

        response = chat_completion.choices[0].message.content
        
        sql_query = extract_sql_query(response)

        if is_unsafe_sql(sql_query):
            raise ValueError("Generated SQL contains unsafe operations.")
        
        explanation_match = re.search(r'```sql.*?```\s*(.*)', response, re.DOTALL)
        explanation = explanation_match.group(1).strip() if explanation_match else "No explanation provided."
        

        return {    
            'success': True,
            'sql': sql_query,
            'error': None,
            'explanation': explanation
        }
        
    except Exception as e:
        return {
            'success': False,
            'sql': None,
            'error': str(e),
            'explanation': "Failed to generate SQL from the natural language query."
        }

def extract_sql_query(text):
    """
    Extract SQL query from text that might contain other text.
    
    Args:
        text (str): Text containing a SQL query
    
    Returns:
        str: The extracted SQL query
    """
    # Look for SQL query between triple backticks
    sql_match = re.search(r'```sql\s*(.*?)\s*```', text, re.DOTALL)
    if sql_match:
        return sql_match.group(1).strip()
    
    # Look for SQL query between single backticks
    sql_match = re.search(r'`(SELECT.*?)`', text, re.DOTALL | re.IGNORECASE)
    if sql_match:
        return sql_match.group(1).strip()
    
    # Look for a query that starts with SELECT
    sql_match = re.search(r'(SELECT.*?)(;|$)', text, re.DOTALL | re.IGNORECASE)
    if sql_match:
        return sql_match.group(1).strip()
    
    # If no SQL query is found, return the original text
    return text.strip()

def is_unsafe_sql(query):
    """
    Check if SQL query contains potentially unsafe operations.
    
    Args:
        query (str): SQL query to check
        
    Returns:
        bool: True if the query is potentially unsafe, False otherwise
    """
    # Check for unsafe operations
    unsafe_patterns = [
        r'\bDROP\b',
        r'\bTRUNCATE\b',
        r'\bDELETE\b',
        r'\bUPDATE\b',
        r'\bINSERT\b',
        r'\bALTER\b',
        r'\bCREATE\b',
        r'\bGRANT\b',
        r'\bREVOKE\b',
        r'\bCOPY\b',
        r';.*?;',  # Multiple statements
        r'--',     # SQL comments
        r'/\*'     # Block comments
    ]
    
    for pattern in unsafe_patterns:
        if re.search(pattern, query, re.IGNORECASE):
            return True
    
    return False
