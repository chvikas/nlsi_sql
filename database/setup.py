import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config import Config

DB_CONFIG = Config.DB_CONFIG

def create_database():
    try:
        # First fix the error by using the correct key from DB_CONFIG
        dbname = DB_CONFIG['database']
        
        # Connect to default PostgreSQL database
        conn = psycopg2.connect(
            host=DB_CONFIG['host'],
            database='postgres', 
            user=DB_CONFIG['user'],
            password=DB_CONFIG['password'],
            port=DB_CONFIG['port']
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conn.cursor()

        # Check if database exists
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
        exists = cursor.fetchone()
        
        if not exists:
            cursor.execute(f"CREATE DATABASE {dbname}")
            print(f"Database {dbname} created successfully")
        else:
            print(f"Database {dbname} already exists")
        
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: {e}")

def setup_tables():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Create departments table with embedding column
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS departments (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            name_embedding TEXT  -- Store embedding as TEXT
        );
        """)
        
        # Create employees table with embedding column
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            department_id INT REFERENCES departments(id),
            email VARCHAR(255) NOT NULL,
            salary DECIMAL(10,2) NOT NULL,
            name_embedding TEXT  -- Store embedding as TEXT
        );
        """)
        
        # Create products table with embedding column
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            price DECIMAL(10,2) NOT NULL,
            name_embedding TEXT  -- Store embedding as TEXT
        );
        """)
        
        # Create orders table with embedding column
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id SERIAL PRIMARY KEY,
            customer_name VARCHAR(100) NOT NULL,
            employee_id INT REFERENCES employees(id),
            order_total DECIMAL(10,2) NOT NULL,
            order_date DATE NOT NULL,
            customer_name_embedding TEXT  -- Store embedding as TEXT
        );
        """)
        
        # Create basic indexes
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_department_id ON employees(department_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_employee_id ON orders(employee_id);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_order_date ON orders(order_date);")
        
        conn.commit()
        print("Database tables created successfully.")

    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'conn' in locals() and conn:
            conn.close()

def initialize_database():
    """Initialize the database."""
    create_database()
    setup_tables()

if __name__ == "__main__":
    initialize_database()