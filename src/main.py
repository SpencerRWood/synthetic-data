from eCommerce_DataGenerator import Visitor, visitor_arrival_times, run_simulation
import simpy 

def main():

    env = simpy.Environment()
    num_visitors = 100  # Number of visitors arriving
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

    all_data = []
    for visitor in visitor_data.value:
        all_data.extend(visitor.data)

    site_events = pd.DataFrame(all_data)

if __name__ == '__main__':
    main()

