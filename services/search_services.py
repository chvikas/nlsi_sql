import pandas as pd

def perform_hybrid_search(conn, sql_query, user_query):
    """Executes the SQL query and returns structured results."""
    if not sql_query:
        return None  # Instead of returning an error string
    
    try:
        with conn.cursor() as cur:
            cur.execute(sql_query)
            rows = cur.fetchall()
            col_names = [desc[0] for desc in cur.description]
            return pd.DataFrame(rows, columns=col_names)
    except Exception as e:
        return None