import pg8000.dbapi
from datetime import datetime
import load_generator

# --- Connection Details (replace with your actual credentials) ---
DB_USER = "postgres"
DB_PASS = "youshallnotpass"
DB_HOST = "localhost"       # e.g., 'localhost' or an IP address
DB_PORT = 5432              # Default PostgreSQL port
DB_NAME = "postgres"

def setup_and_update_metrics():
    """
    Connects to the database, ensures the table exists, and then creates or
    updates the metrics for the 'python' API.
    """
    conn = None
    api_to_track = "python"
    
    print("--- Starting API Metrics Update ---")
    print(f"Target API: {api_to_track}")
    
    try:
        # 1. Connect to the PostgreSQL database
        print("Connecting to the database...")
        conn = pg8000.dbapi.connect(
            user=DB_USER,
            password=DB_PASS,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME
        )
        print("Connection successful.")
        cursor = conn.cursor()

        cursor.execute("SELECT python_count FROM public.request WHERE api_name='go'")
        python_count = cursor.fetchone()[0] + 1

        upsert_query = """
            UPDATE request SET python_count = {} WHERE api_name='go'
        """.format(python_count)
        cursor.execute(upsert_query)
        
        # 4. Commit the transaction to save the changes
        conn.commit()
        #print("Transaction committed successfully.")


    except pg8000.dbapi.Error as e:
        print(e)
        print(f"\n[ERROR] A database error occurred: {e}")
        if conn:
            # Roll back the transaction on error
            conn.rollback()
            print("Transaction has been rolled back.")
            
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred: {e}")

    finally:
        if conn:
            # 6. Close the connection
            conn.close()
            print("\nDatabase connection closed.")

def run_load_generator():
    load_generator.run()

def for_testing():
    return "passed"

if __name__ == "__main__":
    setup_and_update_metrics()
