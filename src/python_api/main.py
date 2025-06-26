import psycopg2
from datetime import datetime
import os
import time
import requests
import signal
import sys
import logging
        
terminate = False
DATABASE_URL = "postgres://postgres:youshallnotpass@postgres-postgresql.postgres.svc.cluster.local:5432/postgres"


def execute_query(query, params=None, fetch=None):
    """
    A helper function to connect, execute a query, and handle resources.
    - query: The SQL query string to execute.
    - params: A tuple of parameters to safely pass to the query.
    - fetch: "one", "all", or None to specify if we should fetch results.
    """
    try:
        # The 'with' statement ensures the connection is always closed
        with psycopg2.connect(DATABASE_URL) as conn:
            # The 'with' statement ensures the cursor is always closed
            with conn.cursor() as cur:
                # Use parameterized queries to prevent SQL injection
                cur.execute(query, params)
                
                # Commit the transaction for write operations
                if fetch is None:
                    conn.commit()
                    logging.info("Query executed and transaction committed.")
                    return True

                logging.info("Query executed successfully.")
                if fetch == "one":
                    return cur.fetchone()
                if fetch == "all":
                    return cur.fetchall()

    except psycopg2.OperationalError as e:
        logging.info(f"Connection Error: Could not connect to the database at '{DATABASE_URL}'.")
        logging.info(f"Detail: {e}")
    except Exception as e:
        logging.info(f"An error occurred: {e}")
    return None

def add_python_count():
    logging.info(os.environ)
    query = "SELECT python_count FROM public.request WHERE api_name='go'"
    logging.info ("query: {}".format(query))
    result = execute_query(query, fetch="one")
    logging.info ("result: {}".format(result))
    if result:
        count = int(result[0]) + 1    
        logging.info ("count: {}".format(count))
        upsert_query = "UPDATE public.request SET python_count = {} WHERE api_name='go'".format(count)
        logging.info ("upsert_query: {}".format(upsert_query))
        execute_query(upsert_query)

def run_load_generator(api_url, delay_ms):
    global terminate
    while not terminate:
        try:
            response = requests.get(api_url)
            logging.info(f"Request to {api_url} completed with status code {response.status_code}")
        except requests.RequestException as e:
            logging.error(f"Request to {api_url} failed: {e}")
        
        time.sleep(delay_ms / 1000.0)
    logging.info("Load generator terminated gracefully.")

def signal_handler(signum, frame):
    global terminate
    logging.info(f"Received signal {signum}, terminating...")
    terminate = True

def run():
    # Configure logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    # Read environment variables
    api_url = os.getenv('API_URL')
    delay_ms = float(os.getenv('DELAY_MS', 1000))  # Default delay to 1000 milliseconds if not set

    if not api_url:
        logging.error("Error: API_URL environment variable is not set.")
        sys.exit(1)

    logging.info("running add_python_count")
    add_python_count()

    # Set up signal handler
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)

    logging.info(f"Starting load generator for {api_url} with a delay of {delay_ms} milliseconds between requests.")
    run_load_generator(api_url, delay_ms)

def for_testing():
    return "passed"

if __name__ == "__main__":
    run()
