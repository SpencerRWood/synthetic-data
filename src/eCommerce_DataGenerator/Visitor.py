#new visitors are defined here as a class
import uuid
import sqlite3
import numpy as np
import random
from datetime import timedelta, datetime
from .Customer import Customer

class Visitor:
    def __init__(self, env, dropoff_probability, customer=None):
        self.env = env
        self.visitor_id = uuid.uuid4() if customer is None else customer.visitor_id
        self.data = []
        self.dropoff_probability = dropoff_probability
        self.customer = customer
        self.is_new_customer = customer is None

    def pageview(self, page):
        current_time = self.get_current_time()
        self.data.append({
            'visitor_id': str(self.visitor_id),
            'page': page,
            'interaction': 'Pageview',
            'element': None,
            'timestamp': current_time
        })
        #print(f"Visitor {self.id} visited the {page} at {self.env.now}.")

    def click(self, page, element):
        current_time = self.get_current_time()
        self.data.append({
            'visitor_id': str(self.visitor_id),
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
        """Convert simulation time (in minutes) to a timestamp in YYYY-MM-DD HH:MM:SS format."""
        current_time = datetime.combine(datetime.today(), datetime.min.time()) + timedelta(minutes=self.env.now)
        return current_time.strftime('%Y-%m-%d %H:%M:%S')
    
    def update_customer_in_db(self, db_name):
        if not self.is_new_customer:  # Only update if this is an existing customer
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            query = '''
            UPDATE customers
            SET purchase_count = ?, last_purchase_time = ?
            WHERE visitor_id = ?;
            '''

            cursor.execute(query, (
                self.customer.purchase_count,
                self.customer.last_purchase_time,
                self.customer.visitor_id
            ))
            conn.commit()
            conn.close()
    
    def insert_new_customer_to_db(self, db_name):
        """Insert the new customer into the database after a purchase."""
        if self.is_new_customer:  # Only insert if this is a new customer
            conn = sqlite3.connect(db_name)
            cursor = conn.cursor()

            query = '''
            INSERT INTO customers (visitor_id, name, gender, age, purchase_count, last_purchase_time, email)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            '''

            cursor.execute(query, (
                self.customer.visitor_id,
                self.customer.name,
                self.customer.gender,
                self.customer.age,
                self.customer.purchase_count,
                self.customer.last_purchase_time,
                self.customer.email
            ))
            conn.commit()
            conn.close()

    def simulate_site_interactions(self, db_name='eCommerce_Simulation.db'):
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
        if not self.customer:
            self.customer = Customer(id=str(self.visitor_id))
        self.customer.make_purchase(self.get_current_time())
        self.insert_new_customer_to_db(db_name)
        self.update_customer_in_db(db_name)
    
        #print(f"Customer {self.customer.id} made a purchase. Total purchases: {self.customer.purchase_count}.")

