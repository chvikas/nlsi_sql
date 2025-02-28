import psycopg2
from psycopg2.extras import RealDictCursor
from config import Config

DB_CONFIG = Config.DB_CONFIG

def get_connection():
    """Get a connection to the PostgreSQL database."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error connecting to database: {e}")
        raise

def execute_query(query, params=None, fetch=True):
    """Execute a SQL query and return the results."""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(query, params)
        
        if fetch:
            results = cursor.fetchall()
            return results
        else:
            conn.commit()
            return cursor.rowcount
            
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"Error executing query: {e}")
        print(f"Query: {query}")
        print(f"Params: {params}")
        raise
    finally:
        if conn:
            conn.close()

def execute_vector_search(table, embedding_field, embedding, limit=5):
    """
    Execute a vector similarity search.
    
    Args:
        table (str): Table name
        embedding_field (str): Field containing the vector embedding
        embedding (list): Vector embedding to compare against
        limit (int): Maximum number of results to return
        
    Returns:
        list: Search results
    """
    query = f"""
    SELECT *, ({embedding_field} <=> %s) AS similarity 
    FROM {table}
    ORDER BY similarity ASC
    LIMIT %s
    """
    
    return execute_query(query, (embedding, limit))

def initialize_db_connection():
    """Test the database connection."""
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.close()
        conn.close()
        print("Database connection successful.")
        return True
    except Exception as e:
        print(f"Database connection failed: {e}")
        return False