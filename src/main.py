from eCommerceGenerator import DayAugmentor, Visitor, Interactions, Customer, NoiseGenerator

def main():
    customer_list = Customer.generate_customers(n=1000)
    ##TODO: make N variable based on the type of day it is
