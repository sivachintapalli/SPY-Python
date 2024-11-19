import psycopg2
from dotenv import load_dotenv
import os
import pandas as pd
from tabulate import tabulate

# Load environment variables
load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST'),
    'database': os.getenv('DB_NAME'),
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD')
}

def get_tables():
    """Get all tables in the database"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Query to get all tables
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        
        tables = cursor.fetchall()
        print("\nAvailable tables:")
        for table in tables:
            print(f"- {table[0]}")
            get_table_structure(table[0])
            print("\nSample data:")
            get_sample_data(table[0])
            print("\n" + "="*50 + "\n")
            
    except Exception as e:
        print(f"Error connecting to database: {e}")
    
    finally:
        cursor.close()
        conn.close()

def get_table_structure(table_name):
    """Get column information for a specific table"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        # Query to get column information
        cursor.execute(f"""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = '{table_name}'
            ORDER BY ordinal_position
        """)
        
        columns = cursor.fetchall()
        print("\nColumn structure:")
        print(tabulate(columns, headers=['Column Name', 'Data Type', 'Nullable'], tablefmt='grid'))
            
    except Exception as e:
        print(f"Error getting table structure: {e}")
    
    finally:
        cursor.close()
        conn.close()

def get_sample_data(table_name, limit=5):
    """Get sample data from the table"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        
        # Using pandas to display the data nicely
        query = f"SELECT * FROM {table_name} LIMIT {limit}"
        df = pd.read_sql(query, conn)
        print(df.to_string())
            
    except Exception as e:
        print(f"Error getting sample data: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    print("Connecting to database and fetching structure...")
    get_tables()
