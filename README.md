Below is a suggested content for your `README.md` file based on the code you provided. It includes an overview, setup instructions, usage details, and other relevant information to help users understand and use your project effectively.

---

# Natural Language Database Search

This project is a Streamlit-based web application that allows users to query a PostgreSQL database using natural language. It leverages AI-powered SQL generation (via the Grok API from xAI), vector embeddings for similarity search (using SentenceTransformers), and a hybrid search approach to provide accurate and user-friendly database querying capabilities.

The application supports querying a database with tables for `employees`, `departments`, `orders`, and `products`, with relationships and embedded vector representations for enhanced search functionality.

## Features
- **Natural Language Queries**: Convert natural language questions (e.g., "Show orders from employees in Engineering") into SQL queries.
- **Vector Similarity Search**: Use precomputed embeddings to match entities (e.g., departments, employees) with user queries.
- **Safe SQL Execution**: Prevent unsafe SQL operations (e.g., `DROP`, `DELETE`) and validate inputs.
- **Interactive UI**: Built with Streamlit for an intuitive user experience.
- **Database Schema**: Includes tables for employees, departments, orders, and products with relationships and embeddings.

## Tech Stack
- **Backend**: Python, PostgreSQL
- **Libraries**: Streamlit, psycopg2, SentenceTransformers, Grok API (via xAI)
- **AI**: Natural language to SQL conversion powered by the Grok API
- **Embeddings**: `all-MiniLM-L6-v2` model from SentenceTransformers

## Prerequisites
- Python 3.8+
- PostgreSQL 13+ with `pgvector` extension installed (for vector similarity search)
- A Grok API key from xAI
- Git (optional, for cloning the repository)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/chvikas/nlsi_sql.git
cd natural-language-db-search
```

### 2. Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

**Note**: Create a `requirements.txt` file with the following content:
```
streamlit
psycopg2-binary
sentence-transformers
groq
python-dotenv
pandas
```

### 4. Configure Environment Variables
Create a `.env` file in the root directory and populate it with your configuration:
```plaintext
DB_HOST=localhost
DB_NAME=your_database_name
DB_USER=your_username
DB_PASSWORD=your_password
DB_PORT=5432
OPENAI_API_KEY=your_api_key
```

### 5. Set Up the Database
1. Ensure PostgreSQL is running and the `pgvector` extension is installed:
   ```sql
   CREATE EXTENSION IF NOT EXISTS vector;
   ```
2. Run the database setup script to create the database and tables:
   ```bash
   python database/setup.py
   ```
3. Seed the database with sample data:
   ```bash
   python database/seed_data.py
   ```

### 6. Run the Application
```bash
streamlit run app.py
```
Open your browser and navigate to `http://localhost:8501`.

## Usage
1. Enter a natural language query in the text box (e.g., "Find all employees in Sales with a salary above 5000").
2. Click the "Search" button.
3. View the results displayed in a table below the input field.
   - If no results are found, a message will indicate this.
   - If an error occurs, an error message will be displayed.

### Example Queries
- "Show orders from employees in Engineering"
- "List products with a price above 1000"
- "Find employees in Marketing with salaries greater than 7000"

## Database Schema
The database consists of the following tables:
1. **employees**: `(id, name, department_id, email, salary, name_embedding)`
2. **departments**: `(id, name, name_embedding)`
3. **orders**: `(id, customer_name, employee_id, order_total, order_date, customer_name_embedding)`
4. **products**: `(id, name, price, name_embedding)`

**Relationships**:
- `employees.department_id` → `departments.id`
- `orders.employee_id` → `employees.id`

**Embeddings**: Stored as `TEXT` (vector embeddings from SentenceTransformers).

## Project Structure
```
natural-language-db-search/
├── app.py                # Streamlit app entry point
├── config.py             # Configuration and schema definition
├── database/             # Database-related scripts
│   ├── connection.py     # Database connection utilities
│   ├── setup.py         # Database creation and table setup
│   └── seed_data.py      # Sample data generation
├── services/             # Core logic and services
│   ├── api_call.py       # Grok API integration
│   ├── query_parser.py   # Natural language to SQL conversion
│   ├── search_services.py# Hybrid search execution
│   └── utils.py          # Utility functions
├── models/               # Embedding model logic
│   └── embedding.py      # SentenceTransformer embedding functions
├── .env                  # Environment variables (not tracked)
└── README.md             # Project documentation
```

## Limitations
- The application only supports `SELECT` queries.
- Vector similarity search requires precomputed embeddings in the database.
- The Grok API key must be valid and properly configured.
- Large datasets may require optimization for performance.

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit your changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- Built with assistance from Grok 3 by xAI.
- Inspired by advancements in natural language processing and database querying.

---

Feel free to customize this further based on your specific repository details (e.g., GitHub URL, license file, etc.). Let me know if you'd like adjustments!