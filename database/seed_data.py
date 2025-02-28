import psycopg2
import random
from datetime import datetime, timedelta
from config import Config
from models.embedding import get_embedding

DB_CONFIG = Config.DB_CONFIG

DEPARTMENTS = [
    "Engineering", "Marketing", "Sales", "Human Resources", 
    "Finance", "Research", "Customer Support", "Operations"
]

FIRST_NAMES = [
    "John", "Jane", "Michael", "Emily", "David", "Sarah", "Robert", "Emma",
    "William", "Olivia", "James", "Sophia", "Joseph", "Isabella", "Thomas", "Mia",
    "Charles", "Charlotte", "Daniel", "Amelia", "Matthew", "Harper", "Andrew", "Evelyn"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White"
]

PRODUCTS = [
    "Laptop", "Desktop Computer", "Smartphone", "Tablet", "Monitor", "Keyboard",
    "Mouse", "Headphones", "Speaker", "Camera", "Printer", "Scanner",
    "External Hard Drive", "USB Flash Drive", "Router", "Modem",
    "Graphics Card", "RAM", "CPU", "Power Supply", "Motherboard",
    "Cooling Fan", "Gaming Console", "VR Headset"
]

CUSTOMERS = [
    "Acme Corp", "Globex", "Initech", "Umbrella Corp", "Stark Industries",
    "Wayne Enterprises", "LexCorp", "Cyberdyne Systems", "Oscorp", "Massive Dynamic",
    "Alias Investigations", "Pied Piper", "Hooli", "Dunder Mifflin", "Soylent Corp",
    "InGen", "Weyland-Yutani", "Tyrell Corporation", "Tricell", "Abstergo Industries"
]

def generate_email(first_name, last_name):
    domains = ["company.com", "example.org", "business.net", "enterprise.co"]
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

def seed_departments(cursor):
    """Seed departments table with sample data."""
    for name in DEPARTMENTS:
        embedding = get_embedding(name)
        cursor.execute(
            "INSERT INTO departments (name, name_embedding) VALUES (%s, %s) RETURNING id",
            (name, embedding)
        )
    
    print(f"Added {len(DEPARTMENTS)} departments")

def seed_employees(cursor, num_employees=50):
    """Seed employees table with sample data."""
    # Get all department IDs
    cursor.execute("SELECT id FROM departments")
    department_ids = [row[0] for row in cursor.fetchall()]
    
    for _ in range(num_employees):
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        name = f"{first_name} {last_name}"
        department_id = random.choice(department_ids)
        email = generate_email(first_name, last_name)
        salary = round(random.uniform(3000, 12000), 2)
        
        embedding = get_embedding(name)
        
        cursor.execute(
            "INSERT INTO employees (name, department_id, email, salary, name_embedding) VALUES (%s, %s, %s, %s, %s)",
            (name, department_id, email, salary, embedding)
        )
    
    print(f"Added {num_employees} employees")

def seed_products(cursor):
    """Seed products table with sample data."""
    for name in PRODUCTS:
        price = round(random.uniform(50, 2000), 2)
        embedding = get_embedding(name)
        
        cursor.execute(
            "INSERT INTO products (name, price, name_embedding) VALUES (%s, %s, %s)",
            (name, price, embedding)
        )
    
    print(f"Added {len(PRODUCTS)} products")

def seed_orders(cursor, num_orders=100):
    """Seed orders table with sample data."""
    # Get all employee IDs
    cursor.execute("SELECT id FROM employees")
    employee_ids = [row[0] for row in cursor.fetchall()]
    
    # Generate random orders
    start_date = datetime.now() - timedelta(days=365)
    end_date = datetime.now()
    
    for _ in range(num_orders):
        customer_name = random.choice(CUSTOMERS)
        employee_id = random.choice(employee_ids)
        order_total = round(random.uniform(100, 5000), 2)
        
        # Random date within the last year
        days_diff = (end_date - start_date).days
        random_days = random.randint(0, days_diff)
        order_date = start_date + timedelta(days=random_days)
        
        embedding = get_embedding(customer_name)
        
        cursor.execute(
            "INSERT INTO orders (customer_name, employee_id, order_total, order_date, customer_name_embedding) VALUES (%s, %s, %s, %s, %s)",
            (customer_name, employee_id, order_total, order_date, embedding)
        )
    
    print(f"Added {num_orders} orders")

def seed_database():
    """Seed the database with sample data."""
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Clear existing data if any
    cursor.execute("TRUNCATE orders, employees, products, departments RESTART IDENTITY CASCADE")
    
    # Seed tables
    seed_departments(cursor)
    seed_employees(cursor)
    seed_products(cursor)
    seed_orders(cursor)
    
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Database seeded successfully!")

if __name__ == "__main__":
    seed_database()