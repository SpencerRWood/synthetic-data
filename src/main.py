from eCommerce_DataGenerator import Visitor, visitor_arrival_times, run_simulation
from eCommerce_DataGenerator import Utils
import simpy 

def main():

    env = simpy.Environment()
    num_visitors = 1000  # Number of visitors arriving
    dropoff_probabilities = {
        'Homepage': 0.1,
        'Product Page': 0.2,
        'View Cart': 0.3,
        'Review Order': 0.4
    }

    # Generate visitor arrival times using a normal distribution centered around 12 PM (720 minutes)
    arrival_times = visitor_arrival_times(num_visitors)

    # Run the simulation
    visitor_data = env.process(run_simulation(env, arrival_times, dropoff_probabilities))
    env.run(until=visitor_data)

    import pandas as pd

    interactions = []
    customer_data = []
    for visitor in visitor_data.value:
        interactions.extend(visitor.data)
        if visitor.customer:
            customer_data.append(visitor.customer.to_dict())

    print(f"Total number of interactions collected: {len(interactions)}")
    print(f"Total number of customers: {len(customer_data)}") 

    
    Utils.load_data_to_db(interactions, customer_data)

if __name__ == '__main__':
    main()

