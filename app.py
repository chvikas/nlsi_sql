import streamlit as st
from database.connection import get_connection
from services.query_parser import natural_language_to_sql
from services.search_services import perform_hybrid_search
from services.utils import validate_query

st.set_page_config(page_title="Natural Language DB Search", layout="wide")
st.title("Natural Language Database Search")
st.markdown("Enter a natural language query to search the PostgreSQL database.")

if "query" not in st.session_state:
    st.session_state.query = ""
if "results" not in st.session_state:
    st.session_state.results = None
if "error" not in st.session_state:
    st.session_state.error = None

user_query = st.text_input(
    "Enter your query (e.g., 'Show orders from employees in Engineering')",
    value=st.session_state.query,
    key="query_input"
)

if st.button("Search"):
    print(user_query)
    if user_query.strip():
        try:
            if not validate_query(user_query):
                print("Invalid query detected.")
                st.session_state.error = "Invalid query detected. Please revise your input."
                st.session_state.results = None
            else:
                print("Validquery detected.")
                conn = get_connection()
                sql_query = natural_language_to_sql(user_query)
                print(f'sql query in app.py {sql_query}')
                results = perform_hybrid_search(conn, sql_query, user_query)
                st.session_state.results = results
                st.session_state.error = None
                st.session_state.query = user_query
                conn.close()
        except Exception as e:
            st.session_state.error = f"An error occurred: {str(e)}"
            st.session_state.results = None
    else:
        st.session_state.error = "Please enter a query."
        st.session_state.results = None

if st.session_state.error:
    st.error(st.session_state.error)
elif st.session_state.results is not None:
    if len(st.session_state.results) > 0:
        st.subheader("Search Results")
        st.dataframe(st.session_state.results)
    else:
        st.info("No results found for your query.")

st.markdown("---")