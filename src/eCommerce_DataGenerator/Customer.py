import uuid
import random
import pandas as pd
from faker import Faker

class Customer:
    def __init__(self, name=None, gender=None, age=None, income=None):
        fake = Faker()
        
        self.id = uuid.uuid4()  # Generate a unique ID for the customer
        self.name = name if name else fake.name()  # Generate a random name if not provided
        self.gender = gender if gender else random.choice(['Male', 'Female'])
        self.age = age if age else random.randint(18, 80)  # Random age between 18 and 80
        self.income = income if income else random.randint(30000, 200000)  # Random income between 30k and 200k
    
    def to_dict(self):
        return {
            'ID': self.id,
            'Name': self.name,
            'Gender': self.gender,
            'Age': self.age,
            'Income': self.income
        }

def generate_customers(n_customers):
    customers = []
    for _ in range(n_customers):
        customer = Customer()
        customers.append(customer.to_dict())
    return customers
