import sqlite3
import random
import simpy
import numpy as np
from .Customer import Customer
from .Visitor import Visitor

def get_returning_customers(n_returning_customers, db_name):
    """
    Queries the database to retrieve a specified number of returning customers using cursor.execute().

    :param n_returning_customers: Number of returning customers to retrieve.
    :param db_name: Path to the SQLite database file.
    :return: List of returning customers as Customer objects.
    """
    print(f"Connecting to database: {db_name}")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM customers')
    count = cursor.fetchone()[0]

    if count == 0:
        # If the table is empty, return an empty list
        print("The customers table is empty. Returning 0 returning customers.")
        conn.close()
        return []

    query = '''
    SELECT visitor_id, return_customer, name, gender, age, purchase_count, last_purchase_time, email
    FROM customers
    ORDER BY RANDOM()
    LIMIT ?;
    '''
    
    cursor.execute(query, (n_returning_customers,))
    rows = cursor.fetchall()
    conn.close()

    # Convert the rows into a list of Customer objects
    returning_customers = [
        Customer(
            visitor_id=row[0],  # Assuming 'ID' is the first column\
            return_customer = row[1],
            name=row[2],  # Assuming 'Name' is the second column
            gender=row[3],  # Assuming 'Gender' is the third column
            age=row[4],  # Assuming 'Age' is the fourth column
            purchase_count=row[5],  # Assuming 'Purchase_Count' is the sixth column
            last_purchase_time=row[6],  # Assuming 'Last_Purchase_Time' is the seventh column
            email=row[7]  # Assuming 'Email' is the eighth column
        )
        for row in rows
    ]

    return returning_customers

def determine_customer(returning_customers):
    """
    Determine whether to use an returning customer or create a new one.

    :param returning_customers: List of returning customers.
    :return: Customer object or None if a new customer should be created.
    """
    if returning_customers:
        return random.choice(returning_customers)
    return None

def visitor_arrival_times(num_visitors, mu=720, sigma=180):
    """Generate visitor arrival times following a normal distribution."""
    arrival_times = np.random.normal(mu, sigma, num_visitors)
    # Clip values to ensure they are within the 0-1440 minute range
    arrival_times = np.clip(arrival_times, 0, 1440)
    return sorted(arrival_times)

def run_simulation(env, n_new_visitors, n_returning_visitors, arrival_times, dropoff_probabilities, returning_customers):
    """Simulates visitors arriving at specific times."""
    visitor_data = []
    for _ in range(n_returning_visitors):
        arrival_time = arrival_times.pop(0)
        delay = arrival_time - env.now
        if delay > 0:
            yield env.timeout(delay)  # Only yield if delay is positive

        customer = determine_customer(returning_customers)
        visitor = Visitor(env, dropoff_probabilities, customer)
        env.process(visitor.simulate_site_interactions())
        visitor_data.append(visitor)

    for _ in range(n_new_visitors):
        arrival_time = arrival_times.pop(0)
        delay = arrival_time - env.now
        if delay > 0:
            yield env.timeout(delay)  # Only yield if delay is positive

        visitor = Visitor(env, dropoff_probabilities)  # New customer
        env.process(visitor.simulate_site_interactions())
        visitor_data.append(visitor)

    return visitor_data
