# from eCommerce_DataGenerator import Visitor
from eCommerce_DataGenerator import Utils
from eCommerce_DataGenerator.Simulation import get_returning_customers, visitor_arrival_times, run_simulation
import simpy
import sqlite3

def main():
    # Configuration
    db_name = 'eCommerce_Simulation.db'  # Path to your SQLite database
    total_visitors = 1000  # Total number of visitors arriving
    returning_customer_ratio = 0.1  # 10% of visitors are returning customers
    
    # Calculate the number of returning and new customers
    n_returning_visitors = int(total_visitors * returning_customer_ratio)
    n_new_visitors = total_visitors - n_returning_visitors
    
    # Get the list of returning customers from the database
    returning_customers = get_returning_customers(n_returning_visitors, db_name)

    # Generate visitor arrival times using a normal distribution centered around 12 PM (720 minutes)
    arrival_times = visitor_arrival_times(total_visitors)

    # Define dropoff probabilities for different pages
    dropoff_probabilities = {
        'Homepage': 0.1,
        'Product Page': 0.2,
        'View Cart': 0.3,
        'Review Order': 0.4
    }

    # Initialize the simulation environment
    env = simpy.Environment()
    
    # Run the simulation
    visitor_data = env.process(run_simulation(env, n_new_visitors, n_returning_visitors, arrival_times, dropoff_probabilities, returning_customers))
    env.run(until=visitor_data)

    # Process the results
    interactions = []
    customer_data = []
    for visitor in visitor_data.value:
        interactions.extend(visitor.data)
        if visitor.customer:
            customer_data.append(visitor.customer.to_dict())

    print(f"Total number of interactions collected: {len(interactions)}")
    print(f"Total number of customers: {len(customer_data)}") 

    # Load data into the database
    conn = sqlite3.connect(db_name)
    Utils.insert_interactions(interactions,conn)
    conn.close()

if __name__ == '__main__':
    main()
