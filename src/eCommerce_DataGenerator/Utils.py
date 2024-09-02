import sqlite3

def insert_interactions(data, conn):
    """
    Inserts interaction data into the SQLite database.
    
    :param data: List of dictionaries containing interaction data.
    :param conn: SQLite connection object.
    """
    cursor = conn.cursor()
    for record in data:
        cursor.execute("""
            INSERT INTO interactions (visitor_id, page, interaction, element, timestamp)
            VALUES (:visitor_id, :page, :interaction, :element, :timestamp)
        """, record)
    conn.commit()

def insert_customers(data, conn):
    """
    Inserts customer data into the SQLite database.
    
    :param data: List of dictionaries containing customer data.
    :param conn: SQLite connection object.
    """
    cursor = conn.cursor()
    for record in data:
        cursor.execute("""
            INSERT INTO customers (ID, Name, Gender, Age, Income, Purchase_Count, Last_Purchase_Time, Email)
            VALUES (:visitor_id, :name, :gender, :age, :purchase_count, :last_purchase_time, :email)
        """, record)
    conn.commit()

def load_data_to_db(all_data, customer_data, db_name="simulation_data.db"):
    """
    Loads interaction and customer data into the SQLite database.
    
    :param all_data: List of dictionaries containing interaction data.
    :param customer_data: List of dictionaries containing customer data.
    :param db_name: Name of the SQLite database file.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    
    try:
        # Insert all_data into the interactions table
        insert_interactions(all_data, conn)
        
        # Insert customer_data into the customers table
        insert_customers(customer_data, conn)
    finally:
        # Close the database connection
        conn.close()

def create_tables(conn):
    cursor = conn.cursor()
    
    # Create interactions table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        visitor_id TEXT,
        page TEXT,
        interaction TEXT,
        element TEXT,
        timestamp TEXT
    )
    """)
    
    # Create customers table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        visitor_id TEXT,
        name TEXT,
        gender TEXT,
        age INTEGER,
        purchase_count INTEGER,
        last_purchase_time TEXT,
        email TEXT
    )
    """)
    
    conn.commit()