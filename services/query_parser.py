from .api_call import call_llm
from .utils import validate_query, sanitize_input
from config import Config
from models.embedding import model, get_embedding  # Import embedding model and function
import psycopg2  # For database connection

SCHEMA = Config.SCHEMA

def get_top_matches(query_embedding, n=3):
    """
    Retrieve the top N matching entities from the database based on vector similarity.
    
    Args:
        query_embedding (list): The embedding vector of the query.
        n (int): Number of top matches to retrieve (default is 3).
    
    Returns:
        list: A list of dictionaries containing name, type, and similarity of top matches.
    """
    print('query_embedding: get top matches')
    print(f"Query embedding sample: {query_embedding[:5]}... (length: {len(query_embedding)})")

    # Ensure pgvector is enabled and query is correct
    sql = """
    SELECT name, type, (name_embedding::vector) <=> %s AS distance
    FROM (
        SELECT name, name_embedding, 'department' AS type FROM departments
        UNION
        SELECT name, name_embedding, 'employee' AS type FROM employees
        UNION
        SELECT name, name_embedding, 'product' AS type FROM products
        UNION
        SELECT customer_name AS name, customer_name_embedding AS name_embedding, 'customer' AS type FROM orders
    ) AS all_entities
    WHERE name_embedding IS NOT NULL
    ORDER BY distance
    LIMIT %s
    """

    try:
        conn = psycopg2.connect(**Config.DB_CONFIG)
        print("Database connection established")
        cur = conn.cursor()

        # Execute the query with debugging
        print("Executing SQL query...")
        cur.execute(sql, (query_embedding, n))
        print("Query executed, fetching results...")
        rows = cur.fetchall()
        top_matches = [{'name': row[0], 'type': row[1], 'similarity': 1 - row[2]} for row in rows]
        print(f"Top matches: {top_matches}")

        cur.close()
        conn.close()
        return top_matches

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        if conn:
            conn.close()
        return []
    except Exception as e:
        print(f"Unexpected error: {e}")
        if conn:
            conn.close()
        return []

# Ensure this integrates with your natural_language_to_sql
def natural_language_to_sql(query_text):
    print('query_text: ', query_text)
    if not validate_query(query_text):
        return {
            'success': False,
            'sql': None,
            'error': 'Invalid query input',
            'explanation': 'Query failed validation checks.'
        }
    
    query_text = sanitize_input(query_text)
    print('sanitized')
    
    # Generate embedding for the query
    query_embedding = get_embedding(model, query_text)
    
    # Get top matches
    top_matches = get_top_matches(query_embedding, n=3)
    
    # Construct match information for the LLM prompt
    match_info = "Top matching entities based on vector similarity:\n"
    for match in top_matches:
        match_info += f"- {match['type'].capitalize()}: '{match['name']}' (similarity: {match['similarity']:.3f})\n"
    
    prompt = f"""
    You are an expert SQL query generator. I'll give you a database schema, a natural language question,
    and top matching entities based on vector similarity. Generate a valid PostgreSQL SQL query.
    
    {SCHEMA}
    
    Top matching entities:
    {match_info}
    
    Question: {query_text}
    
    Rules:
    1. ONLY generate SELECT queries.
    2. Use aliases (e.g., 'e' for employees).
    3. Format dates appropriately for PostgreSQL.
    4. Use exact string matching with the selected entity's name (e.g., WHERE d.name = 'Engineering').
    5. Limit results to 100 rows by default unless specified.
    6. Select the most appropriate entity based on context.
    
    Reply with:
    1. The SQL query between ```sql and ``` tags
    2. An explanation labeled as 'Explanation:' followed by a brief description
    """
    
    response = call_llm(prompt)
    print(response['sql'])
    return response['sql']