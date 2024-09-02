#new visitors are defined here as a class
import uuid
import simpy
import numpy as np
import random
from datetime import timedelta, datetime
from .Customer import Customer

class Visitor:
    def __init__(self, env, dropoff_probability):
        self.env = env
        self.id = uuid.uuid4()
        self.data = []
        self.dropoff_probability = dropoff_probability
        self.customer = None

    def pageview(self, page):
        current_time = self.get_current_time()
        self.data.append({
            'visitor_id': self.id,
            'page': page,
            'interaction': 'Pageview',
            'element': None,
            'timestamp': current_time
        })
        #print(f"Visitor {self.id} visited the {page} at {self.env.now}.")

    def click(self, page, element):
        current_time = self.get_current_time()
        self.data.append({
            'visitor_id': self.id,
            'page': page,
            'interaction': 'Click',
            'element': element,
            'timestamp': current_time
        })
        #print(f"Visitor {self.id} clicked on {element} at {self.env.now}.")
    
    def dropoff(self, page):
        dropoff_probability = self.dropoff_probability.get(page, 0)
        if random.random() < dropoff_probability:
            #print(f"Visitor {self.id} dropped off at {self.env.now} on {page}.")
            return True
        return False
    
    def get_current_time(self):
        """Convert simulation time (in minutes) to a timestamp in HH:MM format."""
        current_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(minutes=self.env.now)
        return current_time.strftime('%H:%M')
    
    def simulate_site_interactions(self):
        self.pageview('Homepage')
        if self.dropoff('Homepage'):
            return
        yield self.env.timeout(1)
        self.click('Homepage', 'Product Page')
        yield self.env.timeout(.2)

        self.pageview('Product Page')
        if self.dropoff('Product Page'):
            return
        yield self.env.timeout(1)
        self.click('Product Page','Add to Cart')
        yield self.env.timeout(.2)
        self.click('Product Page','View Cart')
        yield self.env.timeout(.2)

        self.pageview('View Cart')
        if self.dropoff('View Cart'):
            return
        yield self.env.timeout(1)
        self.click('View Cart','Review Order')
        yield self.env.timeout(.2)

        self.pageview('Review Order')
        if self.dropoff('Review Order'):
            return
        yield self.env.timeout(1)
        self.click('Review Order','Confirm Order')
        yield self.env.timeout(.2)

        self.pageview('Order Confirmation')
        self.customer = Customer(id=self.id)
        self.customer.make_purchase(self.get_current_time())
        #print(f"Customer {self.customer.id} made a purchase. Total purchases: {self.customer.purchase_count}.")

def visitor_arrival_times(num_visitors, mu=720, sigma=180):
    """Generate visitor arrival times following a normal distribution."""
    arrival_times = np.random.normal(mu, sigma, num_visitors)
    # Clip values to ensure they are within the 0-1440 minute range
    arrival_times = np.clip(arrival_times, 0, 1440)
    return sorted(arrival_times)

def run_simulation(env, arrival_times, dropoff_probabilities):
    """Simulates visitors arriving at specific times."""
    visitor_data = []
    for arrival_time in arrival_times:
        delay = arrival_time - env.now
        if delay > 0:
            yield env.timeout(delay)  # Only yield if delay is positive
        visitor = Visitor(env, dropoff_probabilities)
        env.process(visitor.simulate_site_interactions())
        visitor_data.append(visitor)
    return visitor_data

