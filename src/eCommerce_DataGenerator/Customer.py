import uuid
import random
import pandas as pd
from faker import Faker

class Customer:
    def __init__(self, visitor_id, name=None, gender=None, age=None, purchase_count=0, last_purchase_time=None, email=None):
              
        fake = Faker()
        
        self.visitor_id = visitor_id
        self.name = name if name else fake.name()  # Generate a random name if not provided
        self.gender = gender if gender else random.choice(['Male', 'Female'])
        self.age = age if age else random.randint(18, 80)  # Random age between 18 and 80
        self.purchase_count = purchase_count
        self.last_purchase_time = last_purchase_time
        self.email = fake.email()
    
    def make_purchase(self, timestamp):
        self.purchase_count += 1
        self.last_purchase_time = timestamp
    
    def to_dict(self):
        return {
            'visitor_id': self.visitor_id,
            'name': self.name,
            'gender': self.gender,
            'age': self.age,
            'purchase_count': self.purchase_count,
            'last_purchase_time': self.last_purchase_time,
            'email': self.email

        }

