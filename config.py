import os
from dotenv import load_dotenv

load_dotenv()
class Config:

    DB_CONFIG = {
        "host": os.getenv("DB_HOST"),
        "database": os.getenv("DB_NAME"),
        "user": os.getenv("DB_USER"),
        "password": os.getenv("DB_PASSWORD"),
        "port": os.getenv("DB_PORT")
    }

    # OpenAI API key for embeddings and query parsing
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    if not DB_CONFIG["password"]:
        raise ValueError("DB_PASSWORD not found in environment variables")
    
    SCHEMA = """
        Database Schema:
        1. employees (id SERIAL, name VARCHAR, department_id INT, email VARCHAR, salary DECIMAL, name_embedding vector(384))
        2. departments (id SERIAL, name VARCHAR, name_embedding vector(384))
        3. orders (id SERIAL, customer_name VARCHAR, employee_id INT, order_total DECIMAL, order_date DATE, customer_name_embedding vector(384))
        4. products (id SERIAL, name VARCHAR, price DECIMAL, name_embedding vector(384))
        Relationships:
        - employees.department_id -> departments.id
        - orders.employee_id -> employees.id
        """