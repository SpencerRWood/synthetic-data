import sqlite3

##TODO: Add visit, pages counter to customer table

def insert_interactions(data, conn):
    """
    Inserts interaction data into the SQLite database.
    
    :param data: List of dictionaries containing interaction data.
    :param conn: SQLite connection object.
    """
    cursor = conn.cursor()
    for record in data:
        cursor.execute("""
            INSERT INTO interactions (visitor_id, return_customer, page, interaction, element, timestamp)
            VALUES (:visitor_id, :return_customer, :page, :interaction, :element, :timestamp)
        """, record)
    conn.commit()
    print('interactions uploaded')

def create_tables(conn):
    cursor = conn.cursor()
    
    # Create interactions table if it doesn't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS interactions (
        visitor_id TEXT,
        return_customer TEXT,
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
        return_customer TEXT,
        name TEXT,
        gender TEXT,
        age INTEGER,
        purchase_count INTEGER,
        last_purchase_time TEXT,
        email TEXT
    )
    """)
    
    conn.commit()