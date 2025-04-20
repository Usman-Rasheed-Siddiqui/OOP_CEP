
from datetime import datetime

class Rental:
    """A class that represents the data structure for Rental System"""
    def __init__(self, customer, days, vehicle):
        self.customer = customer
        self.vehicle = vehicle
        self.rental_date = datetime.now()
        self.return_date = None
        self.expected_days = days
        self.total_cost = vehicle.price * days
